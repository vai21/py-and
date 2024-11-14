from django.contrib import admin
from django import forms
from django.forms import ModelForm
from import_export import resources
from import_export.admin import ExportActionMixin
from .models import Bp
from customer.models import Customer


# Register your models here.
class BpResource(resources.ModelResource):
    class Meta:
        model = Bp


class BpAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = [
        "id",
        "customer",
        "systolic",
        "diastolic",
        "pulserate",
        "ihb",
        "created_at",
    ]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        group_id = request.user.groups.values_list('id', flat=True).first()
        if not request.user.is_superuser:
            if db_field.name == 'customer':
                kwargs["queryset"] = Customer.objects.filter(group_id=group_id)
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

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ["created_at"]
        return [
            "systolic",
            "diastolic",
            "meanarterialpressure",
            "pulserate",
            "measurement_time",
            "ihb",
            "is_user_move",
            "created_at",
        ]

# Register your models here.
admin.site.register(Bp, BpAdmin)
