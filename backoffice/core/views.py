from rest_framework import viewsets, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from core.models import  (
    User, Project, Dataset, Attribute, Analysis, Visualization
)   
from core.serializers import (
    UserSerializer, ProjectSerializer, DatasetSerializer,
    AnalysisSerializer, VisualizationSerializer, AttributeSerializer
)
from core.constants import *
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



# ---
# API View Classes
# ---


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
     
        # Call sentiment analizer
        sentiment_analyzer = SentimentAnalyzer()
        sentiment_analyzer.analyze_docs(ideas) 

        # Get results
        results = {a:{b:c} for a,b,c in sentiment_analyzer.tagged_docs}
        results = json.dumps(results)

        #save results
        analysis = {'name': request.data['name'], 'project': request.data['project'],
                    'dataset': request.data['dataset'], 'analysis_type': SENTIMENT_ANALYSIS,
                    'result': results}
        
        try: 
            serializer = AnalysisSerializer(data=analysis)
            serializer.is_valid()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            resp = Response(status=status.HTTP_400_BAD_REQUEST)
            resp.content = ex
            return resp


class SentimentAnalysisDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get(self, request, pk, format=None):
        analysis = get_object(Analysis,pk)
        serializer = AnalysisSerializer(analysis)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        try:
            analysis = get_object(Analysis,pk)
            serializer = AnalysisSerializer(analysis, data=request.data)
            serializer.is_valid()
            serializer.save()
            return Response(serializer.data)
        except Exception as ex:
            resp = Response(status=status.HTTP_400_BAD_REQUEST)
            resp.content = ex
            return resp

    def delete(self, request, pk, format=None):
        analysis = get_object(Analysis, pk)
        analysis.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



# ---
# API ViewSet Classes
# ---


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # hash passwords after creating an user
    def perform_create(self, serializer):
        password = make_password(self.request.data['password'])
        serializer.save(password=password)

    # hash passwords after updating an user
    def perform_update(self, serializer):
        password = make_password(self.request.data['password'])
        serializer.save(password=password)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().prefetch_related('dataset')
    serializer_class = ProjectSerializer


class AttributeViewSet(viewsets.ModelViewSet):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer


class DatasetViewSet(viewsets.ModelViewSet):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer


class VisualizationViewSet(viewsets.ModelViewSet):
    queryset = Visualization.objects.all()
    serializer_class = VisualizationSerializer
