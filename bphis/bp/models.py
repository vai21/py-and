from django.db import models

# Create your models here.
class Bp(models.Model):
    name = models.CharField(max_length=200, verbose_name='Patient ID / Patient Name', blank=True)
    systolic = models.CharField(max_length=200, verbose_name='Systolic (SYS)')
    diastolic = models.CharField(max_length=200, verbose_name='Diastolic (DIA)')
    meanarterialpressure = models.CharField(max_length=200, verbose_name='Mean Arterial Pressure (MAP)')
    pulserate = models.CharField(max_length=200, verbose_name='Pulse Rate (PR)')
    created_at = models.DateTimeField(verbose_name='Created At', auto_now_add=True)
