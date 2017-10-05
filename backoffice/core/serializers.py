from core.models import User, Project, Dataset, Visibility
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'username', 'is_superuser', 'password', 'projects')


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name', 'start_date', 'description', 'location', 'people_editing', 'datasets', 'visibilities')


class DatasetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Dataset
        fields = ('id', 'dataset_file', 'dataset_name')


class VisibilitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Visibility
        fields = ('id', 'description')