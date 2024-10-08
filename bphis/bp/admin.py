from django.contrib import admin

from .models import Bp


# Register your models here.
class BpAdmin(admin.ModelAdmin):
    # fields = ["id", "name", "systolic", "diastolic", "meanarterialpressure", "pulserate"]
    list_display = [
        "id",
        "name",
        "systolic",
        "diastolic",
        "meanarterialpressure",
        "pulserate",
    ]


# Register your models here.
admin.site.register(Bp, BpAdmin)
