from django.conf.urls import patterns, url, include
from django.contrib.gis import admin
#from django_extensions.admin import ForeignKeyAutocompleteAdmin

from models import *

admin.site.register(EdigeoBati, admin.ModelAdmin)
admin.site.register(EdigeoBorneParcel, admin.ModelAdmin)
admin.site.register(EdigeoLieuDit, admin.ModelAdmin)
admin.site.register(EdigeoParcelle, admin.ModelAdmin)
admin.site.register(EdigeoSubdFisc, admin.ModelAdmin)