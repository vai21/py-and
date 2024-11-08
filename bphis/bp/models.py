from django.db import models

from datetime import datetime

from customer.models import Customer

# Create your models here.
class Bp(models.Model):
    def __str__(self):
        customer = '-'
        if hasattr(self, 'customer'):
            customer = self.customer
        return f'BP ID:  {self.id} / Customer: {customer} / SYS: {self.systolic} mmHg / DIA: {self.diastolic} mmHg / Pulse: {self.pulserate} / min. / temp: {self.temperature} C / weight: {self.weight}'
        # return self.customer
    
    class Meta:
        ordering = ('-id',)

    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Patient ID', blank=True, null=True, default=None)
    systolic = models.CharField(max_length=200, verbose_name='Systolic (SYS)')
    diastolic = models.CharField(max_length=200, verbose_name='Diastolic (DIA)')
    meanarterialpressure = models.CharField(max_length=200, verbose_name='Mean Arterial Pressure (MAP)')
    pulserate = models.CharField(max_length=200, verbose_name='Pulse Rate (PR)')
    ihb = models.BooleanField(verbose_name="Irregular Heart Beats", blank=True, null=True, default=False)
    temperature = models.FloatField(verbose_name="Body Temperature", blank=True, null=True)
    weight = models.FloatField(verbose_name="Weight", blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='Created At', blank=True, null=True, default=datetime.now)
