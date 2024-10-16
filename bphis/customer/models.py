from django.db import models

from datetime import datetime

# Create your models here.
class Customer(models.Model):
    def __str__(self):
        return self.name

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, verbose_name='Patient Name')
    birthday = models.DateField(verbose_name='Birthday', blank=True)
    gender = models.CharField(max_length=10, verbose_name='Gender')
    idcard = models.CharField(max_length=20, verbose_name='KTP', blank=True)
    mobile = models.CharField(max_length=20, verbose_name='Mobile Number', blank=True)
    blood_type = models.CharField(max_length=2, verbose_name="Blood Type", blank=True)
    profile_pic = models.ImageField(verbose_name="Profile Picture", blank=True, upload_to='static')
    created_at = models.DateTimeField(verbose_name='Created At', default=datetime.now)
