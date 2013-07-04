from models import (EdigeoParcelle, EdigeoLieuDit,
                    EdigeoBati, EdigeoBorneParcel, EdigeoSubdFisc)
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from geoshortcuts.geojson import render_to_geojson


@user_passes_test(lambda u: u.has_perm('staff'))
def subd_fisc(request):
    qs = EdigeoSubdFisc.objects.all()
    json = render_to_geojson(qs, projection=4326)
    return HttpResponse(json, content_type=u'application/json')


@user_passes_test(lambda u: u.has_perm('staff'))
def borne(request):
    qs = EdigeoBorneParcel.objects.all()
    json = render_to_geojson(qs, projection=4326)
    return HttpResponse(json, content_type=u'application/json')


@user_passes_test(lambda u: u.has_perm('staff'))
def bati(request):
    qs = EdigeoBati.objects.all()
    json = render_to_geojson(qs, projection=4326)
    return HttpResponse(json, content_type=u'application/json')


@user_passes_test(lambda u: u.has_perm('staff'))
def parcel(request):
    qs = EdigeoParcelle.objects.all().extra(
        select={'pk': 'gid',
                'supf': 'supf', 'idu': 'idu', 'the_geom': 'the_geom'})
    json = render_to_geojson(qs, projection=4326,
                             properties=[
                                 ('idu', 'idu'), ('supf', 'supf')])
    return HttpResponse(json, content_type=u'application/json')


@user_passes_test(lambda u: u.has_perm('staff'))
def lieudit(request):
    qs = EdigeoLieuDit.objects.all()
    json = render_to_geojson(qs, projection=4326, properties=[
        ('gb_ident', 'gb_ident')])
    return HttpResponse(json, content_type=u'application/json')
