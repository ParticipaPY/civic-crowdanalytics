from rest_framework import serializers
from django.contrib.auth.models import Group, Permission
from core.models import (
    User, Project, Dataset, Attribute, Analysis, 
    Visualization, VisualizationType, Ownership,
    Parameter, Argument
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('__all__')
        extra_kwargs = {'password': {'write_only': True}}


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ('__all__')


class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = '__all__'


class ArgumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Argument
        fields = '__all__'


class AnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analysis
        fields = '__all__'


class VisualizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visualization
        fields = '__all__'

        
class VisualizationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisualizationType
        fields = '__all__'


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
