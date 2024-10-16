from django.db import models

from datetime import datetime

from customer.models import Customer

# Create your models here.
class Bp(models.Model):
    def __str__(self):
        return f'BP ID:  {self.id} / SYS {self.systolic} / DIA {self.diastolic} / Pulse {self.pulserate} '
        # return self.customer
    
    class Meta:
        ordering = ('-id',)

    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Patient ID', blank=True, default=None)
    systolic = models.CharField(max_length=200, verbose_name='Systolic (SYS)')
    diastolic = models.CharField(max_length=200, verbose_name='Diastolic (DIA)')
    meanarterialpressure = models.CharField(max_length=200, verbose_name='Mean Arterial Pressure (MAP)')
    pulserate = models.CharField(max_length=200, verbose_name='Pulse Rate (PR)')
    ihb = models.BooleanField(verbose_name="Irregular Heart Beats", blank=True, default=False)
    created_at = models.DateTimeField(verbose_name='Created At', default=datetime.now)
