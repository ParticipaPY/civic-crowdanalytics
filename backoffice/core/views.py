from rest_framework import viewsets
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.decorators import permission_classes
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group, Permission
from core.models import (
    User, Project, Dataset, Visibility, Analysis, Algorithm, Visualization,
    VisualizationType, Ownership
)
from core.serializers import (
    UserSerializer, ProjectSerializer, DatasetSerializer,
    VisibilitySerializer, AnalysisSerializer, AlgorithmSerializer,
    VisualizationSerializer, VisualizationTypeSerializer, OwnershipSerializer,
    GroupSerializer, PermissionSerializer
)
from core.permissions import CorePermissions, CorePermissionsOrAnonReadOnly


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
class VisibilityViewSet(viewsets.ModelViewSet):
    queryset = Visibility.objects.all()
    serializer_class = VisibilitySerializer


@permission_classes((CorePermissions, ))
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().prefetch_related('dataset')
    serializer_class = ProjectSerializer


@permission_classes((CorePermissions, ))
class DatasetViewSet(viewsets.ModelViewSet):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer


@permission_classes((CorePermissionsOrAnonReadOnly, ))
class AnalysisViewSet(viewsets.ModelViewSet):
    queryset = Analysis.objects.all()
    serializer_class = AnalysisSerializer


@permission_classes((CorePermissionsOrAnonReadOnly, ))
class AlgorithmViewSet(viewsets.ModelViewSet):
    queryset = Algorithm.objects.all()
    serializer_class = AlgorithmSerializer


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
