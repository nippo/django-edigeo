from django.conf.urls import patterns, url

urlpatterns = patterns(
    'edigeo.views',
    url(r'^layers/edigeo/parcelle$', 'parcelle', name='edigeo_parcelle'),
    url(r'^layers/edigeo/subd_fisc$', 'subd_fisc', name='edigeo_subd_fisc'),
    url(r'^layers/edigeo/borne$', 'borne', name='edigeo_borne'),
    url(r'^layers/edigeo/bati$', 'bati', name='edigeo_bati'),
    url(r'^layers/edigeo/lieudit$', 'lieudit', name='edigeo_lieudit')
)
