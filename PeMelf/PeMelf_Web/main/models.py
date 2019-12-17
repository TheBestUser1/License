from django.db import models

class Techniques(models.Model):
    Technique_name = models.CharField(max_length=200)
    Technique_content = models.TextField()


    def __str__(self):
        return self.Technique_name


# Create your models here.
