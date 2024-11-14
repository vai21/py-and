from django.contrib import admin
from django import forms
from django.forms import ModelForm
from .models import Doctor, Patient, SupportingImage
from customer.models import Customer
from bp.models import Bp

# Register your models here.
class SupportingImageInline(admin.TabularInline):
    model = SupportingImage

class PatientAdmin(admin.ModelAdmin):
    inlines = [
      SupportingImageInline,
    ]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        group_id = request.user.groups.values_list('id', flat=True).first()
        if not request.user.is_superuser:
            if db_field.name == 'customer':
                kwargs["queryset"] = Customer.objects.filter(group_id=group_id)
            if db_field.name == 'doctor':
                kwargs["queryset"] = Doctor.objects.filter(group_id=group_id)
            if db_field.name == 'bp':
                kwargs["queryset"] = Bp.objects.filter(group_id=group_id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        group_id = request.user.groups.values_list('id', flat=True).first()
        if request.user.is_superuser:
            return qs
        return qs.filter(group_id=group_id)

    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        group_id = request.user.groups.values_list('id', flat=True).first()
        
        if group_id:
            obj.group_id = group_id
        obj.save()

    list_display = [
        'id',
        'customer',
        'doctor',
        'created_at',
    ]


class DoctorForm(ModelForm):
    class Meta:
        fields = '__all__'
        model = Doctor
        widgets = {
            'gender': forms.Select(choices=[('Male', 'Male'), ('Female', 'Female')]),
        }


class DoctorAdmin(admin.ModelAdmin):
  def get_queryset(self, request):
        qs = super().get_queryset(request)
        group_id = request.user.groups.values_list('id', flat=True).first()
        if request.user.is_superuser:
            return qs
        return qs.filter(group_id=group_id)
    
  def save_model(self, request, obj, form, change):
      """
      Given a model instance save it to the database.
      """
      group_id = request.user.groups.values_list('id', flat=True).first()
        
      if group_id:
          obj.group_id = group_id
      obj.save()
  form = DoctorForm

  list_display = [
     'id',
     'name',
     'title'
  ]

admin.site.register(Patient, PatientAdmin)
admin.site.register(Doctor, DoctorAdmin)
