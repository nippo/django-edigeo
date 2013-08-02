from django.contrib.gis import admin

from models import *

admin.site.register(EdigeoBati, admin.ModelAdmin)
admin.site.register(EdigeoBorneParcel, admin.ModelAdmin)
admin.site.register(EdigeoLieuDit, admin.ModelAdmin)
admin.site.register(Parcelle, admin.ModelAdmin)
admin.site.register(EdigeoSubdFisc, admin.ModelAdmin)
