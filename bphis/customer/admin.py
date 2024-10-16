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

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ["created_at"]
        return []
    form = CustomerForm

# Register your models here.
admin.site.register(Customer, CustomerAdmin)
