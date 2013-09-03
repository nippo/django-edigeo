from models import (EdigeoLieuDit,
                    EdigeoBati, EdigeoBorneParcel, EdigeoSubdFisc)
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from geoshortcuts.geojson import render_to_geojson
from django.views.decorators.gzip import gzip_page


@user_passes_test(lambda u: u.has_perm('staff'))
@gzip_page
def subd_fisc(request):
    qs = EdigeoSubdFisc.objects.all()
    json = render_to_geojson(qs, projection=4326)
    return HttpResponse(json, content_type=u'application/json')


@user_passes_test(lambda u: u.has_perm('staff'))
@gzip_page
def borne(request):
    qs = EdigeoBorneParcel.objects.all()
    json = render_to_geojson(qs, projection=4326)
    return HttpResponse(json, content_type=u'application/json')


@user_passes_test(lambda u: u.has_perm('staff'))
@gzip_page
def bati(request):
    qs = EdigeoBati.objects.all()
    json = render_to_geojson(qs, projection=4326)
    return HttpResponse(json, content_type=u'application/json')


@user_passes_test(lambda u: u.has_perm('staff'))
@gzip_page
def lieudit(request):
    qs = EdigeoLieuDit.objects.all()
    json = render_to_geojson(qs, projection=4326, properties=[
        ('gb_ident', 'gb_ident')],
        #extent=Polygon.from_bbox(bbox).set_srid(4326)
    )
    return HttpResponse(json, content_type=u'application/json')
