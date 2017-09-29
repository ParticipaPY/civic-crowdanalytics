from django.db import models


class Dataset(models.Model):
    dataset_file = models.CharField(max_length=150)
    dataset_name = models.CharField(max_length=50)


class Visibility(models.Model):
    description = models.CharField(max_length=50)


class Project(models.Model):
    name = models.CharField(max_length=250)
    start_date = models.DateTimeField('start date')
    description = models.CharField(max_length=250)
    location = models.CharField(max_length=150)
    people_editing = models.BooleanField()
    datasets = models.ManyToManyField(Dataset)
    visibilities = models.ForeignKey(Visibility, on_delete=models.CASCADE)


class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=254)
    username = models.CharField(max_length=150)
    is_superuser = models.BooleanField()
    password = models.CharField(max_length=32)
    projects = models.ManyToManyField(Project, through='Ownership')


class Ownership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    date_joined = models.DateField()
    owner = models.BooleanField()


class AttributeType(models.Model):
    description = models.CharField(max_length=50)


class Attribute(models.Model):
    attribute_name = models.CharField(max_length=50)
    datasets = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    attribute_types = models.ForeignKey(AttributeType)


class Algorithm(models.Model):
    algorithm_name = models.CharField(max_length=150)


class Analysis(models.Model):
    dataset = models.OneToOneField(Dataset, on_delete=models.CASCADE)
    algorithms = models.ForeignKey(Algorithm, on_delete=models.CASCADE)
    projects = models.ForeignKey(Project, on_delete=models.CASCADE)


class Reports(models.Model):
    analysis = models.ManyToManyField(Analysis)


class VisualizationType(models.Model):
    description = models.CharField(max_length=150)


class Visualization(models.Model):
    payload = models.TextField()
    analysis = models.ForeignKey(Analysis, on_delete=models.CASCADE)
    visualization_types = models.ForeignKey(
        VisualizationType, on_delete=models.CASCADE
    )
