from django.db import models
from datetime import datetime

# Create your models here.
class Doctor(models.Model):
    def __str__(self):
        return self.name

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, verbose_name='Doctor Name')
    birthday = models.DateField(verbose_name='Birthday', blank=True)
    gender = models.CharField(max_length=10, verbose_name='Gender')
    idcard = models.CharField(max_length=20, verbose_name='KTP', blank=True)
    mobile = models.CharField(max_length=20, verbose_name='Mobile Number', blank=True)
    blood_type = models.CharField(max_length=2, verbose_name="Blood Type", blank=True)
    title = models.CharField(max_length=20, verbose_name='Doctor Title', blank=True)
    profile_pic = models.ImageField(verbose_name="Profile Picture", blank=True, upload_to='static')
    created_at = models.DateTimeField(verbose_name='Created At', default=datetime.now)


class Patient(models.Model):
    def __str__(self):
        return self.customer.name
  
    doctor = models.ForeignKey(Doctor, on_delete=models.RESTRICT)
    customer = models.ForeignKey('customer.Customer', on_delete=models.RESTRICT)
    bp = models.ForeignKey('bp.Bp', on_delete=models.DO_NOTHING, default=None, blank=True)
    complain = models.TextField(verbose_name='Patient Complains')
    indication = models.TextField(verbose_name='Doctor Indications')
    medicine = models.CharField(max_length=500, verbose_name='Medicines')
    created_at = models.DateTimeField(verbose_name='Created At', default=datetime.now)

class SupportingImage(models.Model):
    image = models.ImageField(verbose_name="Image")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
