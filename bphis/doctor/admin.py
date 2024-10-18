from django.contrib import admin

from .models import Doctor, Patient, SupportingImage

# Register your models here.
class SupportingImageInline(admin.TabularInline):
    model = SupportingImage

class PatientAdmin(admin.ModelAdmin):
    inlines = [
      SupportingImageInline,
    ]
    list_display = [
        'id',
        'customer',
        'doctor',
        'created_at',
    ]

class DoctorAdmin(admin.ModelAdmin):
  list_display = [
     'id',
     'name',
     'title'
  ]

admin.site.register(Patient, PatientAdmin)
admin.site.register(Doctor, DoctorAdmin)
