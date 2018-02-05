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
    VisualizationType, Parameter, CreationStatus, AnalysisStatus
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
from threading import Thread
import pandas as pd
import numpy as np
import json, os, re, ast
import logging


logger = logging.getLogger(__name__)


# ---
# General methods 
# ---


def inherit_docstring_from(cls):
    """
    Decorator for inherit a docstring
    """
    def docstring_inheriting_decorator(fn):
        fn.__doc__ = getattr(cls,fn.__name__).__doc__
        return fn
    return docstring_inheriting_decorator


def get_object(object, pk):
    """
    Get object from primary key
    """    
    try:
        return object.objects.get(pk=pk)
    except object.DoesNotExist:
        raise Http404


def is_list_of_strings(lst):
    """
    check is a object if of the type list of strings
    """
    return bool(lst) and isinstance(lst, list) and \
    all(isinstance(elem, str) for elem in lst)


def is_list_of_tuples(lst):
    """
    check is a object if of the type list of tuples
    """
    return bool(lst) and isinstance(lst, list) and \
    all(isinstance(elem, tuple) for elem in lst)


def read_stored_dataset(dataset_id, attributes):
    """
    Read dataset instance from dataset_id
    """
    ds = Dataset.objects.get(id=dataset_id)
    ds_file = 'datasets/'+str(ds.file)
    dataset = pd.read_csv(ds_file, sep = None, engine='python')
    dataset = dataset[attributes]
    return dataset


def read_in_memory_dataset(datasetFile, attributes):
    """
    Read in memory dataset
    """
    file_extension = os.path.splitext(datasetFile.name)[1]
    if file_extension == ".csv":
        dataset = pd.read_csv(datasetFile, sep=',')
    if file_extension == ".tsv":
        dataset = pd.read_csv(datasetFile, sep='\t')
    dataset = dataset[attributes]
    return dataset

def read_dataset_from_url(datasetURL, attributes):
    """
    Read dataset from URL
    """
    dataset = pd.read_csv(datasetURL, sep = None, engine='python')
    dataset = dataset[attributes]
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


def create_docs(dataset):
    """
    Create a list of strings from a dataset
    """
    # Drop NA rows
    dataset = dataset.dropna()
    
    # Concat columns
    dataset['concatenation'] = dataset.apply(' '.join, axis=1)

    # Create list of strings
    ds_list = dataset['concatenation'].tolist()  

    return ds_list


def create_dev_docs(dataset):
    """
    Create a list of tuples (text, label) from a dataset
    """
    # Replace NA values to empty string     
    dataset = dataset.replace(np.nan, '', regex=True)

    # Create list of tuples
    lt = [tuple(x) for x in dataset.values]
    ds_list_of_tuples = []
    for tup in lt:
        text = ' '.join(str(tup[i]) for i in range(len(tup)-1))
        label = tup[len(tup)-1]
        ds_list_of_tuples.append((text,label))

    return ds_list_of_tuples


def get_analysis_related_fields(request, analysis_type):
    """
    Get the project_id, dataset_id and arguments from the request
    Create the docs for analysis from the supplied data
    """
    project_id = None
    dataset_id = None
    if request.data.get('parameters'):
        arguments = json.loads(request.data['parameters'])
    else:
        arguments = {}
    if request.data.get('data_object'):
        if analysis_type == DOCUMENT_CLASSIFICATION:
            docs = ast.literal_eval(request.data['data_object'])
            if not is_list_of_tuples(docs):
                raise ValueError('Bad data_object format')    
        else:
            docs = json.loads(request.data['data_object'])
            if not is_list_of_strings(docs):
                raise ValueError('Bad data_object format')    
    else:
        label_column = "label"
        if  request.data.get('project_id') and request.data.get('dataset_id'):
            project_id = request.data['project_id']
            dataset_id = request.data['dataset_id']
            data_columns = get_attributes(dataset_id)
            data_columns = list(data_columns)
            if label_column in data_columns:
                data_columns.remove(label_column)
                data_columns.append(label_column)
            dataset = read_stored_dataset(dataset_id, data_columns)
        else:
            data_columns = json.loads(request.data['data_columns'])
            if label_column in data_columns:
                data_columns.remove(label_column)
                data_columns.append(label_column)
            if 'data_file' in request.data and request.FILES['data_file']:
                data = request.FILES['data_file']
                dataset = read_in_memory_dataset(data, data_columns)
            elif request.data.get('data_url'):
                data = request.data['data_url']
                dataset = read_dataset_from_url(data, data_columns)
        if analysis_type == DOCUMENT_CLASSIFICATION:
            docs = create_dev_docs(dataset)
        else:
            docs = create_docs(dataset)

    return project_id, dataset_id, arguments, docs


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


def save_analysis(analysis, arguments, analysis_type, project_id):
    """
    Save an analysis in the database after is executed
    """
    try: 
        with transaction.atomic():
            # Save analysis
            analysisSerializer = AnalysisSerializer(data=analysis)
            analysisSerializer.is_valid()
            analysisSerializer.save()
            
            # Save arguments
            arguments_list = create_arguments(analysis_type, arguments)
            for arg in arguments_list:
                argumentSerializer = ArgumentSerializer(data=arg)
                argumentSerializer.is_valid()
                argumentSerializer.save()

            # Modify project updated field
            if project_id:
                modify_project_updated_field(project_id)

            return Response(
                analysisSerializer.data, status=status.HTTP_201_CREATED
            )
    except Exception as ex:
        resp = Response(status=status.HTTP_400_BAD_REQUEST)
        resp.content = ex
        return resp


def update_analysis(analysis_id, results):
    """
    Update analysis result and status
    """
    analysis = get_object(Analysis, analysis_id)
    results = json.dumps(results)
    analysis.result = results
    analysis.analysis_status = AnalysisStatus.objects.get(id=EXECUTED)
    analysis.save()


def create_sentiment_analysis_results(arguments, docs, analysis_id):
    """
    Non-blocking thread to create the results of a sentiment analysis
    Change the analysis_status and the results fields of a created analysis
    """
    # Call sentiment analizer
    sa = SentimentAnalyzer(**arguments)
    sa.analyze_docs(docs) 

    # Get results
    results = []
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

    results.append(neg_sentiment)
    results.append(neu_sentiment)
    results.append(pos_sentiment)

    # Update analysis 
    update_analysis(analysis_id, results)
        

def create_document_clustering_results(arguments, docs, analysis_id):
    """
    Non-blocking thread to create the results of a clustering analysis
    Change the analysis_status and the results fields of a created analysis
    """
    # Call document clustering
    dc = DocumentClustering(**arguments)
    dc.clustering(docs)

    # Get results
    results = []
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

    for i in range(dc.num_clusters):
        cluster = {
            "cluster":i, 
            "top_terms": top_terms_clusters[i], 
            "ideas":ideas_clusters[i]
        }
        results.append(cluster)

    # Update analysis 
    update_analysis(analysis_id, results)


def create_concept_extraction_results(arguments, docs, analysis_id):
    """
    Non-blocking thread to create the results of a concept extraction analysis
    Change the analysis_status and the results fields of a created analysis
    """
    # Call concept extractor
    ce = ConceptExtractor(**arguments)
    ce.extract_concepts(docs)

    # Get results
    results = []
    for t in ce.common_concepts:
        concept, occurrences = (t[i] for i in range(2))
        concept_occurrences = {"concept":concept, "occurrences":occurrences}
        results.append(concept_occurrences)

    # Update analysis 
    update_analysis(analysis_id, results)


def create_document_classification_results(arguments, docs, analysis_id):
    """
    Non-blocking thread to create the results of a classification analysis
    Change the analysis_status and the results fields of a created analysis
    """    
    # Call document classifier
    dc = DocumentClassifier(**arguments)
    dc.classify_docs(docs)

    # Get results
    results = []
    ideas_category = {}
    for t in dc.classified_docs:
        doc = t[0]
        category = t[1]
        idea = {"idea":doc}
        if category in ideas_category:
            ideas_category[category].append(idea)
        else:
            ideas_category[category] = [idea]

    for category, ideas_list in ideas_category.items():
        cat = {
            "category":category, 
            "count":len(ideas_list), 
            "ideas": ideas_list
        }
        results.append(cat)

    # Update analysis 
    update_analysis(analysis_id, results)


def post_analysis(request, analysis_type):
    """
    Post an analysis
    """
    # Get analysis related data
    try:    
        project_id, dataset_id, arguments, docs = \
        get_analysis_related_fields(request, analysis_type)
    except Exception as ex:
        response = Response(status=status.HTTP_400_BAD_REQUEST)
        response.content = ex
        return response
   
    analysis_status = IN_PROGRESS
    results = json.dumps([])
    
    # Create analysis
    analysis = {
        'name': request.data['name'], 'project': project_id,
        'dataset': dataset_id, 'analysis_type': analysis_type,
        'analysis_status':analysis_status, 'result': results
    }           
    response = save_analysis(
        analysis, arguments, analysis_type, project_id
    )
   
    # Get target thread function
    if analysis_type ==  SENTIMENT_ANALYSIS:
        target_function = create_sentiment_analysis_results
    elif analysis_type == DOCUMENT_CLUSTERING:
        target_function = create_document_clustering_results
    elif analysis_type == CONCEPT_EXTRACTION:
        target_function = create_concept_extraction_results
    elif analysis_type == DOCUMENT_CLASSIFICATION:
        target_function = create_document_classification_results

    # Create analysis results in a non-blocking thread
    analysis_id = response.data['id']
    analysis_thread = Thread(
        target=target_function, 
        args=(arguments,docs,analysis_id,)
    )
    analysis_thread.setDaemon(True)
    analysis_thread.start()

    return response


# ---
# API View Classes
# ---


class DatasetList(APIView):
    def get(self, request, format=None):
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
        desc: 
        parameters:
        - name: name
          desc: dataset name
          type: string
          required: true
          location: form
        - name: file
          desc: data file
          type: file
          required: true
          location: form
        - name: attributes
          desc: "[
                {
                    \\"name\\":\\"column 1\\"
                    \\"included_in_analysis\\": true
                    \\"attribute_type\\": 1
                },
                {
                    \\"name\\":\\"column 2\\"
                    \\"included_in_analysis\\": true
                    \\"attribute_type\\": 1
                },
                {
                    \\"name\\":\\"column n\\"
                    \\"included_in_analysis\\": true
                    \\"attribute_type\\": 1
                },
            ]"
          type: string
          required: true
          location: form
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
        dataset = get_object(Dataset,pk)
        serializer = DatasetSerializer(dataset)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        dataset = get_object(Dataset, pk)
        dataset.file.delete()
        dataset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProjectList(APIView):
    def get(self, request, format=None):
        try:
            projects = Project.objects.all()
            serializer = ProjectGetSerializer(projects, many=True)
            return Response(serializer.data)
        except Exception as ex:
            resp = Response(status=status.HTTP_400_BAD_REQUEST)
            resp.content = ex
            return resp

    def post(self, request, format=None):
        """
        desc: 
        parameters:
        - name: name
          desc: project name
          type: string
          required: true
          location: form
        - name: description
          desc: project description
          type: string
          required: false
          location: form
        - name: location
          desc: project location
          type: string
          required: false
          location: form
        - name: people_editing
          desc: specifies if a user can edit a project
          type: boolean
          required: false
          location: form
        - name: datasets
          desc: \[dataset_id\]
          type: string
          required: true
          location: form
        - name: visibility
          desc: visibility id
          type: string
          required: false
          location: form
        """

        name = request.data['name']
        description = request.data.get('description',None) or None
        location = request.data.get('location',None) or None
        people_editing = request.data.get('people_editing',False) or False
        datasets = json.loads(request.data['datasets'])
        visibility = request.data.get('visibility',PUBLIC) or PUBLIC
        user_id = request.user.id
        
        project = { 
            'name':name, 
            'description':description,
            'location':location,
            'people_editing':people_editing,
            'datasets':datasets,
            'visibility':visibility,
            'users':[user_id],
            'owner':user_id
        }
    
        # Save project
        serializer = ProjectPostSerializer(data=project)
        serializer.is_valid(raise_exception=True)        
        serializer.save()

        # Update dataset creation status when posting a project
        dataset_id = datasets[0]
        dataset = Dataset.objects.get(id=dataset_id)        
        dataset.creation_status = CreationStatus.objects.get(id=COMPLETED)
        dataset.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProjectDetail(APIView):
    def get(self, request, pk, format=None):
        project = get_object(Project,pk)
        serializer = ProjectGetSerializer(project)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        project = get_object(Project, pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AnalysisObjectList(APIView):
    def post(self, request, format=None):
        """
        desc: 
        parameters:
        - name: name
          desc: Name of the analysis
          type: string
          required: true
          location: form
        - name: parameters
          desc: "{\\"parameter\\":value}"
          type: string
          required: false
          location: form
        - name: project_id
          desc: project id
          type: integer
          required: false
          location: form
        - name: dataset_id
          desc: dataset id
          type: integer
          required: false
          location: form
        - name: data_file
          desc: data file
          type: file
          required: false
          location: form
        - name: data_url
          desc: url of a file
          type: string
          required: false
          location: form
        - name: data_object
          desc: "[\\"text 1\\",\\"text 2\\",\\"text n\\"]"
          type: string
          required: false
          location: form
        - name: data_columns
          desc: "[\\"column 1\\",\\"column 2\\",\\"column n\\"]"
          type: string
          required: false
          location: form
        """


class AnalysisObjectDetail(APIView):
    def get(self, request, pk, format=None):
        analysis = get_object(Analysis,pk)
        serializer = AnalysisSerializer(analysis)
        return Response(serializer.data)


    def delete(self, request, pk, format=None):
        analysis = get_object(Analysis, pk)
        modify_project_updated_field(analysis.project.id)
        analysis.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SentimentAnalysisParamList(APIView):
    def get(self, request, format=None):
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


class DocumentClusteringParamList(APIView):
    def get(self, request, format=None):
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


class DocumentClassificationParamList(APIView):
    def get(self, request, format=None):
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


class SentimentAnalysisList(AnalysisObjectList):   
    def get(self, request, format=None):
        try:
            analysis = Analysis.objects.filter(
                analysis_type=SENTIMENT_ANALYSIS
            )
            serializer = AnalysisSerializer(analysis, many=True)
            return Response(serializer.data)
        except Exception as ex:
            resp = Response(status=status.HTTP_400_BAD_REQUEST)
            resp.content = ex
            return resp

    @inherit_docstring_from(AnalysisObjectList)
    def post(self, request, format=None):
        return post_analysis(request, SENTIMENT_ANALYSIS)


class DocumentClusteringList(AnalysisObjectList):
    def get(self, request, format=None):
        try:
            analysis = Analysis.objects.filter(
                analysis_type=DOCUMENT_CLUSTERING
            )
            serializer = AnalysisSerializer(analysis, many=True)
            return Response(serializer.data)
        except Exception as ex:
            resp = Response(status=status.HTTP_400_BAD_REQUEST)
            resp.content = ex
            return resp

    @inherit_docstring_from(AnalysisObjectList)
    def post(self, request, format=None):
        return post_analysis(request, DOCUMENT_CLUSTERING)


class ConceptExtractionList(AnalysisObjectList):
    def get(self, request, format=None):
        try:
            analysis = Analysis.objects.filter(
                analysis_type=CONCEPT_EXTRACTION
            )
            serializer = AnalysisSerializer(analysis, many=True)
            return Response(serializer.data)
        except Exception as ex:
            resp = Response(status=status.HTTP_400_BAD_REQUEST)
            resp.content = ex
            return resp

    @inherit_docstring_from(AnalysisObjectList)
    def post(self, request, format=None):
        return post_analysis(request, CONCEPT_EXTRACTION)


class DocumentClassificationList(AnalysisObjectList):
    def get(self, request, format=None):
        try:
            analysis = Analysis.objects.filter(
                analysis_type=DOCUMENT_CLASSIFICATION
            )
            serializer = AnalysisSerializer(analysis, many=True)
            return Response(serializer.data)
        except Exception as ex:
            resp = Response(status=status.HTTP_400_BAD_REQUEST)
            resp.content = ex
            return resp

    def post(self, request, format=None):
        """
        desc: 
        parameters:
        - name: name
          desc: Name of the analysis
          type: string
          required: true
          location: form
        - name: parameters
          desc: "{\\"parameter\\":value}"
          type: string
          required: false
          location: form
        - name: project_id
          desc: project id
          type: integer
          required: false
          location: form
        - name: dataset_id
          desc: dataset id
          type: integer
          required: false
          location: form
        - name: data_file
          desc: data file
          type: file
          required: false
          location: form
        - name: data_url
          desc: URL of a file
          type: string
          required: false
          location: form
        - name: data_object
          desc: "[
                    (\\"text 1\\",\\"label 1\\"),
                    (\\"text 2\\",\\"label 2\\"),
                    (\\"text n\\",\\"label n\\")
                ]"
          type: string
          required: false
          location: form
        - name: data_columns
          desc: "[\\"column 1\\",\\"column 2\\",\\"column n\\"]"
          type: string
          required: false
          location: form
        """
        return post_analysis(request, DOCUMENT_CLASSIFICATION)


class SentimentAnalysisDetail(AnalysisObjectDetail): pass
class DocumentClusteringDetail(AnalysisObjectDetail): pass
class ConceptExtractionDetail(AnalysisObjectDetail): pass
class DocumentClassificationDetail(AnalysisObjectDetail): pass


# ---
# API ViewSet Classes
# ---


#@permission_classes((CorePermissions, ))
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

    
"""
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
"""