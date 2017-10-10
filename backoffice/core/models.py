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
    dataset = models.ManyToManyField(Dataset)
    visibility = models.ForeignKey(Visibility, on_delete=models.CASCADE)


class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=254)
    username = models.CharField(max_length=150)
    is_superuser = models.BooleanField()
    password = models.CharField(max_length=100)
    project = models.ManyToManyField(Project, through='Ownership')


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


class Analysis(models.Model):
    dataset = models.OneToOneField(Dataset, on_delete=models.CASCADE)
    algorithm = models.ForeignKey(Algorithm, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class Report(models.Model):
    analysis = models.ManyToManyField(Analysis)


class VisualizationType(models.Model):
    description = models.CharField(max_length=150)


class Visualization(models.Model):
    payload = models.TextField()
    analysis = models.ForeignKey(Analysis, on_delete=models.CASCADE)
    visualization_type = models.ForeignKey(VisualizationType, on_delete=models.CASCADE)
