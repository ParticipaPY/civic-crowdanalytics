from rest_framework import serializers
from django.contrib.auth.models import Group, Permission
from core.models import (
    User, Project, Dataset, Visibility, Analysis, Algorithm, Visualization,
    VisualizationType, Ownership
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'username',
            'is_superuser',
            'password'
        )
        extra_kwargs = {'password': {'write_only': True}}


class VisibilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Visibility
        fields = ('id', 'description')


class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = ('id', 'dataset_name', 'dataset_file')


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = (
            'id',
            'name',
            'start_date',
            'description',
            'location',
            'people_editing',
            'dataset',
            'visibility'
        )


class AlgorithmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Algorithm
        fields = ('id', 'algorithm_name')


class AnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analysis
        fields = '__all__'


class VisualizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visualization
        fields = ('id', 'payload', 'visualization_type', 'analysis')


class VisualizationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisualizationType
        fields = ('id', 'description')


class OwnershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ownership
        fields = ('id', 'user', 'project', 'date_joined', 'owner')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'
