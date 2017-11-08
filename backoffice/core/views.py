from rest_framework import viewsets, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group, Permission
from django.db import transaction
from core.models import (
    User, Project, Dataset, Attribute, Analysis, 
    Visualization, VisualizationType, Ownership,
    Parameter
)
from core.serializers import (
    UserSerializer, ProjectSerializer, DatasetSerializer,
    AnalysisSerializer, VisualizationSerializer, VisualizationTypeSerializer, 
    OwnershipSerializer, GroupSerializer, PermissionSerializer, 
    AttributeSerializer, ArgumentSerializer, ParameterSerializer
)
from core.constants import *
from core.permissions import CorePermissions, CorePermissionsOrAnonReadOnly
from analytics.sentiment_analysis import SentimentAnalyzer 
import pandas as pd
import json
import logging


logger = logging.getLogger(__name__)


# ---
# General methods 
# ---


# Create a list of strings from a dataset
def read_dataset(dataset_id):
    # Get dataset
    ds = Dataset.objects.get(id=dataset_id)
    ds_file = str(ds.file)
        
    # Get dataset attributes that are included for analysis
    attributes = Attribute.objects.filter(dataset_id=dataset_id, included_in_analysis=True)
    attributes = attributes.values_list('name', flat=True)
    
    # Get dataset attributes that have datatype string
    if not attributes:
        attributes = Attribute.objects.filter(dataset_id=dataset_id, attribute_type=STRING)
        attributes = attributes.values_list('name', flat=True)
    
    attributes = list(attributes)
    
    # Import the data
    dataset = pd.read_csv('datasets/'+ds_file, delimiter = '\t', 
                          quoting=3)  # ignore double quotes

    # Select interested columns
    dataset = dataset[attributes]

    # Drop NA rows
    dataset = dataset.dropna()
    
    # Concat columns
    dataset['concatenation'] = dataset.apply(' '.join, axis=1)

    # Create list of strings
    dataset_list = dataset['concatenation'].tolist()  

    return dataset_list


# Get object from primary key
def get_object(object, pk):
    try:
        return object.objects.get(pk=pk)
    except object.DoesNotExist:
        raise Http404


# Create a list of arguments for an analysis
# It uses the arguments passed as parameters.
# If some argument is not supplied, 
# it uses de default value in the parameters table
def create_arguments(analysis_type, arguments):
    arguments_list = []
    parameters = Parameter.objects.filter(analysis_type_id = analysis_type)
    for p in parameters:
        if p.name in arguments:
            value = arguments[p.name]
        else:
            value = p.default_value
        parameter_id = p.id
        analysis_id = Analysis.objects.latest('id').id
        argument = {
            'value':value, 
            'parameter':parameter_id,
            'analysis':analysis_id
        }
        arguments_list.append(argument)
    return arguments_list


# ---
# API View Classes
# ---

class SentimentAnalysisParamList(APIView):
    """
    List all parameters for sentiment analysis.
    """
    def get(self, request, format=None):
        try:
            parameters = Parameter.objects.filter(analysis_type=SENTIMENT_ANALYSIS)
            serializer = ParameterSerializer(parameters, many=True)
            return Response(serializer.data)
        except Exception as ex:
            resp = Response(status=status.HTTP_400_BAD_REQUEST)
            resp.content = ex
            return resp


class SentimentAnalysisList(APIView):
    """
    List all sentiment analysis, or create a new sentiment analysis.
    """
    def get(self, request, format=None):
        try:
            analysis = Analysis.objects.filter(analysis_type=SENTIMENT_ANALYSIS)
            serializer = AnalysisSerializer(analysis, many=True)
            return Response(serializer.data)
        except Exception as ex:
            resp = Response(status=status.HTTP_400_BAD_REQUEST)
            resp.content = ex
            return resp

    def post(self, request, format=None):
        try:    
            ideas = read_dataset(request.data['dataset'])
        except Exception as ex:
            resp = Response(status=status.HTTP_400_BAD_REQUEST)
            resp.content = ex
            return resp

        # Get arguments
        arguments = request.data['arguments']

        # Call sentiment analizer
        sentiment_analyzer = SentimentAnalyzer(**arguments)
        sentiment_analyzer.analyze_docs(ideas) 

        # Get results
        results = {a:{b:c} for a,b,c in sentiment_analyzer.tagged_docs}
        results = json.dumps(results)

        # Set status to Executed
        analysis_status = EXECUTED

        #save results
        analysis = {
            'name': request.data['name'], 'project': request.data['project'],
            'dataset': request.data['dataset'], 'analysis_type': SENTIMENT_ANALYSIS,
            'analysis_status':analysis_status, 'result': results
        }            
        
        try: 
            with transaction.atomic():
                # Save analysis
                analysisSerializer = AnalysisSerializer(data=analysis)
                analysisSerializer.is_valid()
                analysisSerializer.save()
                
                # Save arguments
                arguments_list = create_arguments(SENTIMENT_ANALYSIS, arguments)
                for arg in arguments_list:
                    argumentSerializer = ArgumentSerializer(data=arg)
                    argumentSerializer.is_valid()
                    argumentSerializer.save()
                
                return Response(analysisSerializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            resp = Response(status=status.HTTP_400_BAD_REQUEST)
            resp.content = ex
            return resp


class SentimentAnalysisDetail(APIView):
    """
    Retrieve or delete a sentiment analysis instance.
    """
    def get(self, request, pk, format=None):
        analysis = get_object(Analysis,pk)
        serializer = AnalysisSerializer(analysis)
        return Response(serializer.data)


    def delete(self, request, pk, format=None):
        analysis = get_object(Analysis, pk)
        analysis.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



# ---
# API ViewSet Classes
# ---
@permission_classes((CorePermissions, ))
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # hash passwords after creating an user
    def perform_create(self, serializer):
        password = make_password(self.request.data['password'])
        serializer.save(password=password)

    # hash passwords after updating an user
    def perform_update(self, serializer):
        if 'password' in self.request.data:
            password = make_password(self.request.data['password'])
            serializer.save(password=password)
        else:
            serializer.save()


@permission_classes((CorePermissions, ))
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().prefetch_related('dataset')
    serializer_class = ProjectSerializer

    
@permission_classes((CorePermissions, ))
class AttributeViewSet(viewsets.ModelViewSet):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer


@permission_classes((CorePermissions, ))
class DatasetViewSet(viewsets.ModelViewSet):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer


@permission_classes((CorePermissionsOrAnonReadOnly, ))
class AnalysisViewSet(viewsets.ModelViewSet):
    queryset = Analysis.objects.all()
    serializer_class = AnalysisSerializer

    
@permission_classes((CorePermissions, ))
class VisualizationViewSet(viewsets.ModelViewSet):
    queryset = Visualization.objects.all()
    serializer_class = VisualizationSerializer


@permission_classes((CorePermissions, ))
class VisualizationTypeViewSet(viewsets.ModelViewSet):
    queryset = VisualizationType.objects.all()
    serializer_class = VisualizationTypeSerializer


@permission_classes((CorePermissions, ))
class OwnershipViewSet(viewsets.ModelViewSet):
    queryset = Ownership.objects.all()
    serializer_class = OwnershipSerializer


@permission_classes((CorePermissions, ))
class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


@permission_classes((CorePermissions, ))
class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer