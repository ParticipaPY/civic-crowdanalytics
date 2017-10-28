from rest_framework import serializers
from core.models import (
    User, Project, Dataset, Attribute, Analysis, Visualization,
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


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ('__all__')


class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = ('id', 'name', 'file')


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


class AnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analysis
        fields = '__all__'


class VisualizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visualization
        fields = ('id', 'payload', 'visualization_type', 'analysis')

