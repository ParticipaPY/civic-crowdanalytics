from rest_framework import viewsets
from rest_framework.parsers import FormParser, MultiPartParser
from core.models import User, Project, Dataset, Visibility
from core.serializers import UserSerializer, ProjectSerializer, DatasetSerializer, VisibilitySerializer
from django.contrib.auth.hashers import make_password

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    #hash passwords after creating an user
    def perform_create(self, serializer):
        password = make_password(self.request.data['password'])
        serializer.save(password=password)

    #hash passwords after updating an user
    def perform_update(self, serializer):
        password = make_password(self.request.data['password'])
        serializer.save(password=password)

class VisibilityViewSet(viewsets.ModelViewSet):
    queryset = Visibility.objects.all()
    serializer_class = VisibilitySerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class DatasetViewSet(viewsets.ModelViewSet):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer

