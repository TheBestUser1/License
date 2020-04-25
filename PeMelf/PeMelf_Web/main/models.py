from django.db import models
from django import forms

class Techniques(models.Model):
    Technique_name = models.CharField(max_length=200)
    Technique_content = models.TextField()
    Technique_script = models.CharField(max_length=20)

    def __str__(self):
        return self.Technique_name


class Document(models.Model):
    title = models.CharField(max_length=50)
    date_added = models.DateTimeField('date published')
    myfile = models.FileField()
    user_token=models.CharField(max_length=200)

    def __str__(self):
        return self.title

class Document_download(models.Model):
    name = models.CharField(max_length=50)
    path_to_file = models.CharField(max_length=250)
    user_token=models.CharField(max_length=200)

    def __str__(self):
        return self.name
# Create your models here.
