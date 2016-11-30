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
    pass
