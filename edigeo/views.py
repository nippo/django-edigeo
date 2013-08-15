from models import (Parcelle, EdigeoLieuDit,
                    EdigeoBati, EdigeoBorneParcel, EdigeoSubdFisc)
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from geoshortcuts.geojson import render_to_geojson
from django.contrib.gis.geos import Polygon
import ast
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
def parcel(request):
    qs = Parcelle.objects.all()
    bbox = ast.literal_eval(
        '(' + request.GET.get('bbox', '-160, -89, 160, 89') + ')')

    polygon = Polygon.from_bbox(bbox)
    polygon.set_srid(4326)
    polygon.transform(900913)
    json = render_to_geojson(
        qs,
        projection=4326,
        properties=[
            ('idu', 'idu'), ('supf', 'supf')],
        #extent=polygon
    )
    return HttpResponse(json, content_type=u'application/json')


@user_passes_test(lambda u: u.has_perm('staff'))
@gzip_page
def lieudit(request):
    qs = EdigeoLieuDit.objects.all()
    bbox = ast.literal_eval(
        "(" + request.GET.get('bbox', '(0, 180, 0, 180)') + ")")
    json = render_to_geojson(qs, projection=4326, properties=[
        ('gb_ident', 'gb_ident')],
        extent=Polygon.from_bbox(bbox).set_srid(4326)
    )
    return HttpResponse(json, content_type=u'application/json')
