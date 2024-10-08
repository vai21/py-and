from django.db import models

# Create your models here.
class Bp(models.Model):
    name = models.CharField(max_length=200)
    systolic = models.CharField(max_length=200)
    diastolic = models.CharField(max_length=200)
    meanarterialpressure = models.CharField(max_length=200)
    pulserate = models.CharField(max_length=200)
