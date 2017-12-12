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
    attributes = AttributeSerializer(many=True, read_only=True)

    class Meta:
        model = Dataset
        fields = ('id','name','file','creation_status','attributes')


class ParameterSerializer(serializers.ModelSerializer):
    parameter_type = serializers.SlugRelatedField(read_only=True, slug_field='description')

    class Meta:
        model = Parameter
        fields = ('name','parameter_type','default_value')


class ArgumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Argument
        fields = '__all__'


class AnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analysis
        fields = '__all__'


class ProjectAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analysis
        fields = ('id','analysis_type','analysis_status')


class ProjectSerializer(serializers.ModelSerializer):
    analysis = ProjectAnalysisSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = (
            'id', 'name', 'start_date', 'description', 'location', 
            'people_editing', 'dataset', 'visibility', 'analysis'
        )


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
