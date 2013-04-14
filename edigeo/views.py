from models import (EdigeoParcelle, EdigeoLieuDit,
                    EdigeoBati, EdigeoBorneParcel, EdigeoSubdFisc)
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from geoshortcuts.geojson import render_to_geojson


@user_passes_test(lambda u: u.has_perm('staff'))
def subd_fisc(request):
    qs = EdigeoSubdFisc.objects.all()
    json = render_to_geojson(qs, projection=4326)
    return HttpResponse(json, mimetype=u'application/json')


@user_passes_test(lambda u: u.has_perm('staff'))
def borne(request):
    qs = EdigeoBorneParcel.objects.all()
    json = render_to_geojson(qs, projection=4326)
    return HttpResponse(json, mimetype=u'application/json')


@user_passes_test(lambda u: u.has_perm('staff'))
def bati(request):
    qs = EdigeoBati.objects.all()
    json = render_to_geojson(qs, projection=4326)
    return HttpResponse(json, mimetype=u'application/json')


@user_passes_test(lambda u: u.has_perm('staff'))
def parcel(request):
    qs = EdigeoParcelle.objects.all()
    json = render_to_geojson(qs, projection=4326, properties=['idu', 'supf'])
    return HttpResponse(json, mimetype=u'application/json')


@user_passes_test(lambda u: u.has_perm('staff'))
def lieudit(request):
    qs = EdigeoLieuDit.objects.all()
    json = render_to_geojson(qs, projection=4326, properties=['gb_ident'])
    return HttpResponse(json, mimetype=u'application/json')
