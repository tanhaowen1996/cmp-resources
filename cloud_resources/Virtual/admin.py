from django.contrib import admin
from .models import Nfs


# Register your models here.

@admin.register(Nfs)
class NfsAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'name',
                    'path',
                    'status',
                    'quota',
                    'used')
