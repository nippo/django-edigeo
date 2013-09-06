from django.contrib.gis.db import models
from cad.models import Insee, Section, Lieudit


class EdigeoBati(models.Model):
    gid = models.IntegerField(primary_key=True)
    gb_ident = models.CharField(max_length=40, blank=True)
    gb_idnum = models.IntegerField(null=True, blank=True)
    dur = models.CharField(max_length=80, blank=True)
    the_geom = models.GeometryField(null=True, blank=True)

    class Meta:
        db_table = u'edigeo_bati'


class EdigeoBorneParcel(models.Model):
    gid = models.IntegerField(primary_key=True)
    gb_ident = models.CharField(max_length=40, blank=True)
    gb_idnum = models.IntegerField(null=True, blank=True)
    the_geom = models.GeometryField(null=True, blank=True)

    class Meta:
        db_table = u'edigeo_borne_parcel'


class EdigeoLieuDit(models.Model):
    gid = models.IntegerField(primary_key=True)
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
    the_geom = models.GeometryField(null=True, blank=True)
    objects = models.GeoManager()

    class Meta:
        db_table = u'edigeo_lieu_dit'


class Parcelle(models.Model):
    gid = models.IntegerField(primary_key=True)
    insee = models.ForeignKey(Insee, null=True)
    section = models.ForeignKey(Section, null=True)
    lieudit = models.ForeignKey(Lieudit, null=True)
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
    the_geom = models.GeometryField(null=True, blank=True, srid=900913)
    objects = models.GeoManager()

    def __unicode__(self):
        return u'%s' % (self.idu)

    class Meta:
        db_table = u'edigeo_parcelle'


class EdigeoSubdFisc(models.Model):
    gid = models.IntegerField(primary_key=True)
    gb_ident = models.CharField(max_length=40, blank=True)
    gb_idnum = models.IntegerField(null=True, blank=True)
    tex = models.CharField(max_length=80, blank=True)
    the_geom = models.GeometryField(null=True, blank=True)

    class Meta:
        db_table = u'edigeo_subd_fisc'
