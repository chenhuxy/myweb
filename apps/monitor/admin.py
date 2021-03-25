from django.contrib import admin
from .models import *
# Register your models here.
class HostAdmin(admin.ModelAdmin):
    list_display = ('hostid','ip','createdate','lastmodified')





admin.site.register(Host,HostAdmin)