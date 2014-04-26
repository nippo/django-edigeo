from django.contrib.gis.db import models
from cad.models import Insee

edigeobati_mapping = {
    'gb_ident': 'GB_IDENT',
    'gb_idnum': 'GB_IDNUM',
    'dur': 'DUR',
    'the_geom': 'MULTIPOLYGON',
}

class EdigeoBati(models.Model):
    gb_ident = models.CharField(max_length=40, blank=True)
    gb_idnum = models.IntegerField(null=True, blank=True)
    dur = models.CharField(max_length=80, blank=True)
    the_geom = models.GeometryField(srid=3857)

    class Meta:
        db_table = u'edigeo_bati'


edigeoborneparcel_mapping = {
    'gb_ident': 'GB_IDENT',
    'gb_idnum': 'GB_IDNUM',
    'the_geom': 'MULTIPOLYGON',
}


class EdigeoBorneParcel(models.Model):
    gb_ident = models.CharField(max_length=40, blank=True)
    gb_idnum = models.IntegerField(null=True, blank=True)
    the_geom = models.GeometryField(srid=3857)

    class Meta:
        db_table = u'edigeo_borne_parcel'


edigeolieudit_mapping = {
    'gb_ident': 'GB_IDENT',
    'gb_idnum': 'GB_IDNUM',
    'tex10': 'TEX10',
    'tex2': 'TEX2',
    'tex3': 'TEX3',
    'tex4': 'TEX4',
    'tex5': 'TEX5',
    'tex6': 'TEX6',
    'tex7': 'TEX7',
    'tex8': 'TEX8',
    'tex9': 'TEX9',
    'tex': 'TEX',
    'the_geom': 'MULTIPOLYGON',
}


class EdigeoLieuDit(models.Model):
    gb_ident = models.CharField(max_length=40, blank=True)
    gb_idnum = models.IntegerField(null=True, blank=True)
    tex10 = models.CharField(max_length=80, blank=True)
    tex2 = models.CharField(max_length=80, blank=True)
    tex3 = models.CharField(max_length=80, blank=True)
    tex4 = models.CharField(max_length=80, blank=True)
    tex5 = models.CharField(max_length=80, blank=True)
    tex6 = models.CharField(max_length=80, blank=True)
    tex7 = models.CharField(max_length=80, blank=True)
    tex8 = models.CharField(max_length=80, blank=True)
    tex9 = models.CharField(max_length=80, blank=True)
    tex = models.CharField(max_length=80, blank=True)
    the_geom = models.GeometryField(srid=3857)
    objects = models.GeoManager()

    class Meta:
        db_table = u'edigeo_lieu_dit'


edigeoparcelle_mapping = {
    'gb_ident': 'GB_IDENT',
    'gb_idnum': 'GB_IDNUM',
    'coar': 'COAR',
    'codm': 'CODM',
    'idu': 'IDU',
    'indp': 'INDP',
    'supf': 'SUPF',
    'tex2': 'TEX2',
    'tex': 'TEX',
    'the_geom': 'MULTIPOLYGON',
}

class EdigeoParcelle(models.Model):
    insee = models.ForeignKey(Insee, null=True)
    gb_ident = models.CharField(max_length=40, blank=True)
    gb_idnum = models.IntegerField(null=True, blank=True)
    coar = models.CharField(max_length=1, blank=True)
    codm = models.CharField(max_length=80, blank=True)
    idu = models.CharField(max_length=20, blank=True)
    indp = models.CharField(max_length=80, blank=True)
    supf = models.DecimalField(null=True, max_digits=8,
                               decimal_places=2, blank=True)
    tex2 = models.CharField(max_length=80, blank=True)
    tex = models.CharField(max_length=80, blank=True)
    the_geom = models.GeometryField(srid=3857)
    objects = models.GeoManager()

    def __unicode__(self):
        return u'%s' % (self.idu)

    class Meta:
        db_table = u'edigeo_parcelle'


edigeosubdfisc_mapping = {
    'gb_ident': 'GB_IDENT',
    'gb_idnum': 'GB_IDNUM',
    'tex': 'TEX',
    'the_geom': 'MULTIPOLYGON',
}

class EdigeoSubdFisc(models.Model):
    gb_ident = models.CharField(max_length=40, blank=True)
    gb_idnum = models.IntegerField(null=True, blank=True)
    tex = models.CharField(max_length=80, blank=True)
    the_geom = models.GeometryField(srid=3857)

    class Meta:
        db_table = u'edigeo_subd_fisc'
