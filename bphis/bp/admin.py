from django.contrib import admin
from import_export import resources
from import_export.admin import ExportActionMixin
from .models import Bp


# Register your models here.
class BpResource(resources.ModelResource):
    class Meta:
        model = Bp
class BpAdmin(ExportActionMixin, admin.ModelAdmin):

    list_display = [
        "id",
        
        "customer_id",
        "systolic",
        "diastolic",
        "pulserate",
        "ihb",
        "created_at",
    ]

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ["created_at"]
        return [
            "systolic",
            "diastolic",
            "meanarterialpressure",
            "pulserate",
            "created_at",
        ]

# Register your models here.
admin.site.register(Bp, BpAdmin)
