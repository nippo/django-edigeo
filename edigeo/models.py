from django.contrib.gis.db import models


class EdigeoCommune(models.Model):
    idu = models.CharField(unique=True, max_length=100)
    gb_ident = models.CharField(max_length=80, blank=True, unique=True)
    the_geom = models.GeometryField(srid=3857)
    objects = models.GeoManager()

    class Meta:
        db_table = u'edigeo_commune'


class EdigeoSection(models.Model):
    idu = models.CharField(unique=True, max_length=100)
    tex = models.CharField(max_length=80, blank=True)
    the_geom = models.GeometryField(srid=3857)
    objects = models.GeoManager()

    class Meta:
        db_table = u'edigeo_section'


class EdigeoLieuDit(models.Model):
    tex = models.CharField(max_length=80, blank=True)
    md5 = models.CharField(max_length=80, blank=True, unique=True)
    the_geom = models.GeometryField(srid=3857)
    objects = models.GeoManager()

    class Meta:
        db_table = u'edigeo_lieu_dit'


class EdigeoParcelle(models.Model):
    idu = models.CharField(max_length=20, blank=True, unique=True)
    commune_idu = models.CharField(max_length=20, blank=True, null=True)
    section_idu = models.CharField(max_length=20, blank=True, null=True)
    supf = models.DecimalField(null=True, max_digits=8,
                               decimal_places=2, blank=True)
    tex = models.CharField(max_length=80, blank=True)
    the_geom = models.GeometryField(srid=3857)
    objects = models.GeoManager()

    def __str__(self):
        return u'%s' % (self.idu)

    class Meta:
        db_table = u'edigeo_parcelle'


class EdigeoSubdFisc(models.Model):
    tex = models.CharField(max_length=80, blank=True)
    md5 = models.CharField(max_length=80, blank=True, unique=True)
    the_geom = models.GeometryField(srid=3857)

    class Meta:
        db_table = u'edigeo_subd_fisc'


class EdigeoBorneParcel(models.Model):
    the_geom = models.GeometryField(srid=3857)

    class Meta:
        db_table = u'edigeo_borne_parcel'


class EdigeoBati(models.Model):
    the_geom = models.GeometryField(srid=3857)

    class Meta:
        db_table = u'edigeo_bati'
