from rest_framework import viewsets, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group, Permission
from django.db import transaction
from django.shortcuts import get_object_or_404
from core.models import (
    User, Project, Dataset, Attribute, Analysis, Visualization, 
    VisualizationType, Parameter, CreationStatus
)
from core.serializers import (
    UserSerializer, DatasetSerializer, ProjectGetSerializer, 
    ProjectPostSerializer, AnalysisSerializer, VisualizationSerializer, 
    VisualizationTypeSerializer, GroupSerializer, PermissionSerializer, 
    AttributeSerializer, ArgumentSerializer, ParameterSerializer,
)
from core.constants import *
from core.permissions import CorePermissions, CorePermissionsOrAnonReadOnly
from analytics.sentiment_analysis import SentimentAnalyzer
from analytics.clustering import DocumentClustering
from analytics.concept_extraction import ConceptExtractor
from analytics.classification import DocumentClassifier
from datetime import datetime
import pandas as pd
import numpy as np
import json
import logging


logger = logging.getLogger(__name__)


# ---
# General methods 
# ---


def get_object(object, pk):
    """
    Get object from primary key
    """    
    try:
        return object.objects.get(pk=pk)
    except object.DoesNotExist:
        raise Http404


def get_dataset(dataset_id):
    """
    Get dataset instance from dataset_id
    """
    ds = Dataset.objects.get(id=dataset_id)
    ds_file = 'datasets/'+str(ds.file)
    dataset = pd.read_csv(ds_file, sep = None, engine='python')
    return dataset


def get_attributes(dataset_id):
    """
    Get dataset attributes as a queryset from dataset_id
    """
    # Get dataset attributes that are included for analysis
    attributes = Attribute.objects.filter(
        dataset_id=dataset_id, 
        included_in_analysis=True
    )
    
    # Get dataset attributes that have datatype string
    if not attributes:
        attributes = Attribute.objects.filter(
            dataset_id=dataset_id, 
            attribute_type=STRING
        )
    
    attributes = attributes.values_list('name', flat=True)

    return attributes


def modify_project_updated_field(project_id):
    """
    Update the updated field of a project with the current time
    """
    project = get_object(Project, project_id)
    project.update_date = datetime.now()
    project.save()


def create_docs(dataset_id):
    """
    Create a list of strings from a dataset
    """
    dataset = get_dataset(dataset_id)
    attributes = get_attributes(dataset_id)
    attributes = list(attributes)    

    # Select interested columns
    dataset = dataset[attributes]

    # Drop NA rows
    dataset = dataset.dropna()
    
    # Concat columns
    dataset['concatenation'] = dataset.apply(' '.join, axis=1)

    # Create list of strings
    dataset_list = dataset['concatenation'].tolist()  

    return dataset_list


def create_dev_docs(dataset_id, label_column="label"):
    """
    Create a list of tuples (text, label) from a dataset
    """
    dataset = get_dataset(dataset_id)
    attributes = get_attributes(dataset_id)

    # Get label column
    label = attributes.filter(name=label_column)
    label = label.values_list('name', flat=True)
    label = list(label)

    # Get text column
    text = attributes.exclude(name=label_column)
    text = text.values_list('name', flat=True)    
    text = list(text)

    # Select interested columns
    dataset = dataset[text+label]

    # Replace NA values to empty string     
    dataset = dataset.replace(np.nan, '', regex=True)

    # Create list of tuples
    lt = [tuple(x) for x in dataset.values]
    list_of_tuples = []
    for tup in lt:
        text = ' '.join(str(tup[i]) for i in range(len(tup)-1))
        label = tup[len(tup)-1]
        list_of_tuples.append((text,label))

    return list_of_tuples


def create_arguments(analysis_type, arguments):
    """
    Create a list of arguments for an analysis
    It uses the arguments passed as parameters.
    If some argument is not supplied, 
    it uses de default value in the parameters table
    """
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


class AnalysisObjectDetail(APIView):
    def get(self, request, pk, format=None):
        """
        Retrieve an analysis object instance
        """
        analysis = get_object(Analysis,pk)
        serializer = AnalysisSerializer(analysis)
        return Response(serializer.data)


    def delete(self, request, pk, format=None):
        """
        Delete an analysis object instance
        """
        analysis = get_object(Analysis, pk)
        modify_project_updated_field(analysis.project.id)
        analysis.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SentimentAnalysisParamList(APIView):
    def get(self, request, format=None):
        """
        List all parameters for sentiment analysis
        """
        try:
            parameters = Parameter.objects.filter(
                analysis_type=SENTIMENT_ANALYSIS
            )
            serializer = ParameterSerializer(parameters, many=True)
            return Response(serializer.data)
        except Exception as ex:
            resp = Response(status=status.HTTP_400_BAD_REQUEST)
            resp.content = ex
            return resp


class DocumentClassificationParamList(APIView):
    def get(self, request, format=None):
        """
        List all parameters for document classification
        """
        try:
            parameters = Parameter.objects.filter(
                analysis_type=DOCUMENT_CLASSIFICATION
            )
            serializer = ParameterSerializer(parameters, many=True)
            return Response(serializer.data)
        except Exception as ex:
            resp = Response(status=status.HTTP_400_BAD_REQUEST)
            resp.content = ex
            return resp


class DocumentClusteringParamList(APIView):
    def get(self, request, format=None):
        """
        List all parameters for document clustering
        """
        try:
            parameters = Parameter.objects.filter(
                analysis_type=DOCUMENT_CLUSTERING
            )
            serializer = ParameterSerializer(parameters, many=True)
            return Response(serializer.data)
        except Exception as ex:
            resp = Response(status=status.HTTP_400_BAD_REQUEST)
            resp.content = ex
            return resp


class ConceptExtractionParamList(APIView):
    def get(self, request, format=None):
        """
        List all parameters for concept extraction
        """
        try:
            parameters = Parameter.objects.filter(
                analysis_type=CONCEPT_EXTRACTION
            )
            serializer = ParameterSerializer(parameters, many=True)
            return Response(serializer.data)
        except Exception as ex:
            resp = Response(status=status.HTTP_400_BAD_REQUEST)
            resp.content = ex
            return resp


class SentimentAnalysisList(APIView):
    def get(self, request, format=None):
        """
        List all sentiment analysis
        """
        try:
            analysis = Analysis.objects.filter(analysis_type=SENTIMENT_ANALYSIS)
            serializer = AnalysisSerializer(analysis, many=True)
            return Response(serializer.data)
        except Exception as ex:
            resp = Response(status=status.HTTP_400_BAD_REQUEST)
            resp.content = ex
            return resp

    def post(self, request, format=None):
        """
        Create a new sentiment analysis
        """
        # Get project_id and dataset if they are supplied
        if  'project_id' in request.data and request.data['project_id'] and \
            'dataset_id' in request.data and request.data['dataset_id']:
            project_id = request.data['project_id']
            dataset_id = request.data['dataset_id']
            try:    
                ideas = create_docs(dataset_id)
            except Exception as ex:
                resp = Response(status=status.HTTP_400_BAD_REQUEST)
                resp.content = ex
                return resp
        else:
            project_id = None
            dataset_id = None

        #######################################################

        # Get analysis parameters
        if 'parameters' in request.data and request.data['parameters']:
            arguments = json.loads(request.data['parameters'])
        else:
            arguments = {}

        # Call sentiment analizer
        sa = SentimentAnalyzer(**arguments)
        sa.analyze_docs(ideas) 

        # Get results
        neg_ideas = []
        neu_ideas = []
        pos_ideas = []
        for t in sa.tagged_docs:            
            doc, sentiment, score = (t[i] for i in range(3))
            idea = {"idea":doc, "score":score}
            if sentiment == "neg":
                neg_ideas.append(idea)
            if sentiment == "neu":
                neu_ideas.append(idea)
            if sentiment == "pos":
                pos_ideas.append(idea)

        neg_sentiment = {"sentiment":"neg", "ideas":neg_ideas}
        neu_sentiment = {"sentiment":"neu", "ideas":neu_ideas}
        pos_sentiment = {"sentiment":"pos", "ideas":pos_ideas}

        results = [neg_sentiment,neu_sentiment,pos_sentiment]
        results = json.dumps(results)

        # Set status to Executed
        analysis_status = EXECUTED

        #save results
        analysis = {
            'name': request.data['name'], 'project': project_id,
            'dataset': dataset_id, 'analysis_type': SENTIMENT_ANALYSIS,
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

                # Modify project updated field
                if project_id:
                    modify_project_updated_field(project_id)

                return Response(analysisSerializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            resp = Response(status=status.HTTP_400_BAD_REQUEST)
            resp.content = ex
            return resp


class DocumentClassificationList(APIView):
    def get(self, request, format=None):
        """
        List all document classification analysis
        """
        try:
            analysis = Analysis.objects.filter(analysis_type=DOCUMENT_CLASSIFICATION)
            serializer = AnalysisSerializer(analysis, many=True)
            return Response(serializer.data)
        except Exception as ex:
            resp = Response(status=status.HTTP_400_BAD_REQUEST)
            resp.content = ex
            return resp

    def post(self, request, format=None):
        """
        Create a new document classification analysis
        """
        try:    
            dev_docs = create_dev_docs(request.data['dataset'])
        except Exception as ex:
            resp = Response(status=status.HTTP_400_BAD_REQUEST)
            resp.content = ex
            return resp

        # Get arguments
        arguments = request.data['arguments']
        
        # Call document classifier
        dc = DocumentClassifier(**arguments)
        dc.classify_docs(dev_docs)

        # Get results
        ideas_category = {}
        for t in dc.classified_docs:
            doc = t[0]
            category = t[1]
            idea = {"idea":doc}
            if category in ideas_category:
                ideas_category[category].append(idea)
            else:
                ideas_category[category] = [idea]

        results = []
        for category, ideas_list in ideas_category.items():
            cat = {"category":category, "count":len(ideas_list), "ideas": ideas_list}
            results.append(cat)
        results = json.dumps(results)        

        # Set status to Executed
        analysis_status = EXECUTED

        #save results
        analysis = {
            'name': request.data['name'], 'project': request.data['project'],
            'dataset': request.data['dataset'], 'analysis_type': DOCUMENT_CLASSIFICATION,
            'analysis_status':analysis_status, 'result': results
        }            
        
        try: 
            with transaction.atomic():
                # Save analysis
                analysisSerializer = AnalysisSerializer(data=analysis)
                analysisSerializer.is_valid()
                analysisSerializer.save()
                
                # Save arguments
                arguments_list = create_arguments(DOCUMENT_CLASSIFICATION, arguments)
                for arg in arguments_list:
                    argumentSerializer = ArgumentSerializer(data=arg)
                    argumentSerializer.is_valid()
                    argumentSerializer.save()

                # Modify project updated field
                modify_project_updated_field(request.data['project'])
                
                return Response(analysisSerializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            resp = Response(status=status.HTTP_400_BAD_REQUEST)
            resp.content = ex
            return resp


class DocumentClusteringList(APIView):
    def get(self, request, format=None):
        """
        List all clustering analysis
        """
        try:
            analysis = Analysis.objects.filter(analysis_type=DOCUMENT_CLUSTERING)
            serializer = AnalysisSerializer(analysis, many=True)
            return Response(serializer.data)
        except Exception as ex:
            resp = Response(status=status.HTTP_400_BAD_REQUEST)
            resp.content = ex
            return resp

    def post(self, request, format=None):
        """
        Create a new clustering analysis
        """
        try:    
            docs = create_docs(request.data['dataset'])
        except Exception as ex:
            resp = Response(status=status.HTTP_400_BAD_REQUEST)
            resp.content = ex
            return resp

        # Get arguments
        arguments = request.data['arguments']

        # Call document clustering
        dc = DocumentClustering(**arguments)
        dc.clustering(docs)

        # Get results
        vec = dc.get_coordinate_vectors()
        ideas_clusters = [[] for x in range(dc.num_clusters)] 
        num_docs = len(vec["docs"])
        for i in range(num_docs):
            doc = vec["docs"][i]            
            x = vec["x"][i]
            y = vec["y"][i]
            cluster = vec["label"][i]
            idea = {"idea":doc, "posx":x, "posy":y}
            ideas_clusters[cluster].append(idea) 
        
        top_terms = dc.top_terms_per_cluster()
        top_terms_clusters = [[] for x in range(dc.num_clusters)]
        for cluster in range(dc.num_clusters):
            for tup in top_terms[str(cluster)]:
                term = tup[0]
                score = tup[1]
                top_term = {"term":term, "score":score}
                top_terms_clusters[cluster].append(top_term)

        results = []
        for i in range(dc.num_clusters):
            cluster = {
                "cluster":i, 
                "top_terms": top_terms_clusters[i], 
                "ideas":ideas_clusters[i]
            }
            results.append(cluster)
        results = json.dumps(results)

        # Set status to Executed
        analysis_status = EXECUTED

        #save results
        analysis = {
            'name': request.data['name'], 'project': request.data['project'],
            'dataset': request.data['dataset'], 'analysis_type': DOCUMENT_CLUSTERING,
            'analysis_status':analysis_status, 'result': results
        }            
        
        try: 
            with transaction.atomic():
                # Save analysis
                analysisSerializer = AnalysisSerializer(data=analysis)
                analysisSerializer.is_valid()
                analysisSerializer.save()
                
                # Save arguments
                arguments_list = create_arguments(DOCUMENT_CLUSTERING, arguments)
                for arg in arguments_list:
                    argumentSerializer = ArgumentSerializer(data=arg)
                    argumentSerializer.is_valid()
                    argumentSerializer.save()

                # Modify project updated field
                modify_project_updated_field(request.data['project'])
                
                return Response(analysisSerializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            resp = Response(status=status.HTTP_400_BAD_REQUEST)
            resp.content = ex
            return resp


class ConceptExtractionList(APIView):
    def get(self, request, format=None):
        """
        List all concept extraction analysis
        """
        try:
            analysis = Analysis.objects.filter(analysis_type=CONCEPT_EXTRACTION)
            serializer = AnalysisSerializer(analysis, many=True)
            return Response(serializer.data)
        except Exception as ex:
            resp = Response(status=status.HTTP_400_BAD_REQUEST)
            resp.content = ex
            return resp

    def post(self, request, format=None):
        """
        Create a new concept extraction analysis
        """
        try:    
            docs = create_docs(request.data['dataset'])
        except Exception as ex:
            resp = Response(status=status.HTTP_400_BAD_REQUEST)
            resp.content = ex
            return resp

        # Get arguments
        arguments = request.data['arguments']

        # Call concept extractor
        ce = ConceptExtractor(**arguments)
        ce.extract_concepts(docs)

        # Get results
        results = []
        for t in ce.common_concepts:
            concept, occurrences = (t[i] for i in range(2))
            concept_occurrences = {"concept":concept, "occurrences":occurrences}
            results.append(concept_occurrences)
        results = json.dumps(results)
       
        # Set status to Executed
        analysis_status = EXECUTED

        #save results
        analysis = {
            'name': request.data['name'], 'project': request.data['project'],
            'dataset': request.data['dataset'], 'analysis_type': CONCEPT_EXTRACTION,
            'analysis_status':analysis_status, 'result': results
        }            
        
        try: 
            with transaction.atomic():
                # Save analysis
                analysisSerializer = AnalysisSerializer(data=analysis)
                analysisSerializer.is_valid()
                analysisSerializer.save()
                
                # Save arguments
                arguments_list = create_arguments(CONCEPT_EXTRACTION, arguments)
                for arg in arguments_list:
                    argumentSerializer = ArgumentSerializer(data=arg)
                    argumentSerializer.is_valid()
                    argumentSerializer.save()

                # Modify project updated field
                modify_project_updated_field(request.data['project'])
                
                return Response(analysisSerializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            resp = Response(status=status.HTTP_400_BAD_REQUEST)
            resp.content = ex
            return resp


class SentimentAnalysisDetail(AnalysisObjectDetail): pass
class DocumentClassificationDetail(AnalysisObjectDetail): pass
class DocumentClusteringDetail(AnalysisObjectDetail): pass
class ConceptExtractionDetail(AnalysisObjectDetail): pass


class DatasetList(APIView):
    def get(self, request, format=None):
        """
        List all datasets
        """
        try:
            datasets = Dataset.objects.all()
            serializer = DatasetSerializer(datasets, many=True)
            return Response(serializer.data)
        except Exception as ex:
            resp = Response(status=status.HTTP_400_BAD_REQUEST)
            resp.content = ex
            return resp

    def post(self, request, format=None):
        """
        Create a new dataset and his associated attributes
        """
        # Get request data
        dataset = {
            'name': request.data['name'], 'file': request.data['file']
        }            
        attributes = json.loads(request.data['attributes'])
        
        try: 
            with transaction.atomic():
                # Save dataset
                datasetSerializer = DatasetSerializer(data=dataset)
                datasetSerializer.is_valid()
                datasetSerializer.save()
                
                # Save attributes
                for attr in attributes:
                    dataset_id = Dataset.objects.latest('id').id
                    attr.update({'dataset':dataset_id})
                    attributeSerializer = AttributeSerializer(data=attr)
                    attributeSerializer.is_valid()
                    attributeSerializer.save()
                
                return Response(datasetSerializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            resp = Response(status=status.HTTP_400_BAD_REQUEST)
            resp.content = ex
            return resp


class DatasetDetail(APIView):
    def get(self, request, pk, format=None):
        """
        Retrieve a dataset instance
        """
        dataset = get_object(Dataset,pk)
        serializer = DatasetSerializer(dataset)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        """
        Delete a dataset instance
        """
        dataset = get_object(Dataset, pk)
        dataset.file.delete()
        dataset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ---
# API ViewSet Classes
# ---


@permission_classes((CorePermissions, ))
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        """
        Hash passwords after creating an user
        """
        password = make_password(self.request.data['password'])
        serializer.save(password=password)

    def perform_update(self, serializer):
        """
        Hash passwords after updating an user
        """
        if 'password' in self.request.data:
            password = make_password(self.request.data['password'])
            serializer.save(password=password)
        else:
            serializer.save()


class ProjectViewSet(viewsets.ViewSet):
    def list(self, request):
        """
        List all projects
        """
        queryset = Project.objects.all()
        serializer = ProjectGetSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Retrieve a project instance
        """
        queryset = Project.objects.all()
        project = get_object_or_404(queryset, pk=pk)
        serializer = ProjectGetSerializer(project)
        return Response(serializer.data)
    
    def create(self, request):
        """
        Create a new project
        """
        # Use the current user as user and owner of the project        
        request.data['users'] = [request.user.id]
        request.data['owner'] = request.user.id
        
        # Save project
        serializer = ProjectPostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)        
        serializer.save()

        # Update dataset creation status when posting a project
        dataset_id = self.request.data['datasets'][0]
        dataset = Dataset.objects.get(id=dataset_id)        
        dataset.creation_status = CreationStatus.objects.get(id=COMPLETED)
        dataset.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        """
        Delete a project instance
        """
        queryset = Project.objects.all()
        project = get_object_or_404(queryset, pk=pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
@permission_classes((CorePermissions, ))
class AttributeViewSet(viewsets.ModelViewSet):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer


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
class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


@permission_classes((CorePermissions, ))
class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer