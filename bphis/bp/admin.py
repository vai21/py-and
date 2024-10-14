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
