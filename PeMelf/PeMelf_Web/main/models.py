from django.db import models
from django import forms

class Techniques(models.Model):
    Technique_name = models.CharField(max_length=200)
    Technique_content = models.TextField()

    def __str__(self):
        return self.Technique_name


class Document(models.Model):
    title = models.CharField(max_length=50)
    myfile = models.FileField()

    def __str__(self):
        return self.title
# Create your models here.
