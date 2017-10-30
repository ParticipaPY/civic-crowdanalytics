from django.db import models
from django.contrib.auth.models import AbstractUser


class Dataset(models.Model):
    dataset_name = models.CharField(max_length=50)
    dataset_file = models.FileField()

    def __str__(self):
        return self.dataset_name


class Visibility(models.Model):
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.description


class Project(models.Model):
    name = models.CharField(max_length=250)
    start_date = models.DateTimeField(auto_now_add=True, blank=True)
    description = models.CharField(max_length=250)
    location = models.CharField(max_length=150)
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
    attribute_name = models.CharField(max_length=50)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    attribute_type = models.ForeignKey(AttributeType)


class Algorithm(models.Model):
    algorithm_name = models.CharField(max_length=150)

    def __str__(self):
        return self.algorithm_name


class Analysis(models.Model):
    name = models.CharField(max_length=100, default='Analysis1')
    dataset = models.OneToOneField(Dataset, on_delete=models.CASCADE)
    algorithm = models.ForeignKey(Algorithm, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


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
