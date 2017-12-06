from django.db import models
from django_mysql.models import JSONField
from django.contrib.auth.models import AbstractUser
from core.constants import *


class CreationStatus(models.Model):
    description = models.CharField(max_length=150)


class Dataset(models.Model):
    name = models.CharField(max_length=50)
    file = models.FileField()
    creation_status = models.ForeignKey(CreationStatus, on_delete=models.CASCADE, default=DRAFT)

    def __str__(self):
        return self.name


class Visibility(models.Model):
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.description


class Project(models.Model):
    name = models.CharField(max_length=250)
    start_date = models.DateTimeField(auto_now_add=True, blank=True)
    description = models.CharField(max_length=250, blank=True)
    location = models.CharField(max_length=150, blank=True)
    people_editing = models.BooleanField()
    dataset = models.ManyToManyField(Dataset)
    visibility = models.ForeignKey(Visibility, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class User(AbstractUser):
    project = models.ManyToManyField(Project, through='Ownership')

    def __str__(self):
        return self.username


class Ownership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    date_joined = models.DateField()
    owner = models.BooleanField()


class AttributeType(models.Model):
    description = models.CharField(max_length=50)


class Attribute(models.Model):
    name = models.CharField(max_length=50)
    included_in_analysis = models.BooleanField()
    dataset = models.ForeignKey(Dataset, related_name='attributes', on_delete=models.CASCADE)
    attribute_type = models.ForeignKey(AttributeType)


class AnalysisType(models.Model):
    description = models.CharField(max_length=150)


class AnalysisStatus(models.Model):
    description = models.CharField(max_length=150)


class ParameterType(models.Model):
    description = models.CharField(max_length=150)


class Parameter(models.Model):
    name = models.CharField(max_length=150)
    default_value = models.CharField(max_length=150)
    parameter_type = models.ForeignKey(ParameterType, on_delete=models.CASCADE)
    analysis_type = models.ForeignKey(AnalysisType, on_delete=models.CASCADE)


class Analysis(models.Model):
    name = models.CharField(max_length=150)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    analysis_type = models.ForeignKey(AnalysisType, on_delete=models.CASCADE)
    analysis_status = models.ForeignKey(AnalysisStatus, on_delete=models.CASCADE)
    result = JSONField()

    def __str__(self):
        return self.name


class Argument(models.Model):
    value = models.CharField(max_length=150)
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE)
    analysis = models.ForeignKey(Analysis, on_delete=models.CASCADE)


class Report(models.Model):
    analysis = models.ManyToManyField(Analysis)


class VisualizationType(models.Model):
    description = models.CharField(max_length=150)

    def __str__(self):
        return self.description


class Visualization(models.Model):
    payload = models.TextField()
    analysis = models.ForeignKey(Analysis, on_delete=models.CASCADE)
    visualization_type = models.ForeignKey( 
        VisualizationType,
        on_delete=models.CASCADE
    )
