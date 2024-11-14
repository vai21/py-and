from django.contrib import admin

from django import forms
from django.forms import ModelForm

from .models import Customer


# Register your models here.

class CustomerForm(ModelForm):
    class Meta:
        fields = '__all__'
        model = Customer
        widgets = {
            'gender': forms.Select(choices=[('Male', 'Male'), ('Female', 'Female')]),
        }


class CustomerAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "birthday",
        "gender",
        "idcard",
        "mobile",
        "blood_type",
        "profile_pic",
        "created_at",
    ]

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
        return []
    form = CustomerForm

# Register your models here.
admin.site.register(Customer, CustomerAdmin)
