from rest_framework import viewsets, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from core.models import (
    User, Project, Dataset, Visibility, Analysis, Algorithm, Visualization,
    VisualizationType
)
from core.serializers import (
    UserSerializer, ProjectSerializer, DatasetSerializer,
    VisibilitySerializer, AnalysisSerializer, AlgorithmSerializer,
    VisualizationSerializer, VisualizationTypeSerializer
)
import pandas as pd
from analytics.sentiment_analysis import SentimentAnalyzer 
import json
import logging

logger = logging.getLogger(__name__)

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


class VisibilityViewSet(viewsets.ModelViewSet):
    queryset = Visibility.objects.all()
    serializer_class = VisibilitySerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().prefetch_related('dataset')
    serializer_class = ProjectSerializer


class DatasetViewSet(viewsets.ModelViewSet):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer


class AnalysisViewSet(viewsets.ModelViewSet):
    queryset = Analysis.objects.all()
    serializer_class = AnalysisSerializer

    def create(self, request):
    
        # Get dataset
        ds_id = request.data['dataset']
        ds = Dataset.objects.get(id=ds_id)
        ds_file = str(ds.dataset_file)
        
        # Import the data
        dataset = pd.read_csv('datasets/'+ds_file, delimiter = '\t', 
                              quoting=3)  # ignore double quotes

        # Select interested columns
        dataset = dataset[['title', 'text']]
        
        # Drop NA rows
        dataset = dataset.dropna()
        
        # Put ideas into a list
        ideas = dataset['text'].tolist()        

        # Call sentiment analizer
        sentiment_analyzer = SentimentAnalyzer()
        sentiment_analyzer.analyze_docs(ideas) 

        # Get results
        results = {a:{b:c} for a,b,c in sentiment_analyzer.tagged_docs}
        results = json.dumps(results)

        #save results
        analysis = {'name': request.data['name'],'dataset': request.data['dataset'], 
                    'algorithm': request.data['algorithm'], 'project': request.data['project'],
                    'result': results}
        #logger.info(analysis)
        
        serializer = AnalysisSerializer(data=analysis)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class AlgorithmViewSet(viewsets.ModelViewSet):
    queryset = Algorithm.objects.all()
    serializer_class = AlgorithmSerializer


class VisualizationViewSet(viewsets.ModelViewSet):
    queryset = Visualization.objects.all()
    serializer_class = VisualizationSerializer


class VisualizationTypeViewSet(viewsets.ModelViewSet):
    queryset = VisualizationType.objects.all()
    serializer_class = VisualizationTypeSerializer
