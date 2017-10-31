from rest_framework import serializers
from core.models import (
    User, Project, Dataset, Attribute, Analysis, Visualization,
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


class AnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analysis
        fields = '__all__'


class VisualizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visualization
        fields = '__all__'

