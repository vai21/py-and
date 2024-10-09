from django.contrib import admin

from .models import Bp


# Register your models here.
class BpAdmin(admin.ModelAdmin):
    # fields = ["id", "name", "systolic", "diastolic", "meanarterialpressure", "pulserate"]
    list_display = [
        "name",
        "systolic",
        "diastolic",
        "meanarterialpressure",
        "pulserate",
    ]
    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return []
        return ['systolic', 'diastolic', 'meanarterialpressure', 'pulserate']

# Register your models here.
admin.site.register(Bp, BpAdmin)
