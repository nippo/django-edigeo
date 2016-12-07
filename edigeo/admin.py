from .models import EdigeoCommune
from .models import EdigeoSection
from .models import EdigeoLieuDit
from .models import EdigeoParcelle
from .models import EdigeoSubdFisc
from .models import EdigeoBati
from .models import EdigeoBorneParcel
from django.contrib import admin


@admin.register(EdigeoCommune)
class EdigeoCommuneAdmin(admin.ModelAdmin):
    list_display = (
        'idu',
        'gb_ident'
    )


@admin.register(EdigeoSection)
class EdigeoSectionAdmin(admin.ModelAdmin):
    search_fields = ['idu', 'tex']
    list_display = (
        'idu',
        'tex'
    )


@admin.register(EdigeoLieuDit)
class EdigeoLieuDitAdmin(admin.ModelAdmin):
    list_display = (
        'tex',
        'md5'
    )


@admin.register(EdigeoParcelle)
class EdigeoParcelleAdmin(admin.ModelAdmin):
    list_display = (
        'idu',
        'supf',
        'tex',
        'section_idu',
        'commune_idu'
    )


@admin.register(EdigeoSubdFisc)
class EdigeoSubdFiscAdmin(admin.ModelAdmin):
    list_display = (
        'tex',
        'md5'
    )
