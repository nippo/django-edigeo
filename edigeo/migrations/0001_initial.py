# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        (b'cad', b'__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name=b'EdigeoSubdFisc',
            fields=[
                (b'gid', models.IntegerField(serialize=False, primary_key=True)),
                (b'gb_ident', models.CharField(max_length=40, blank=True)),
                (b'gb_idnum', models.IntegerField(null=True, blank=True)),
                (b'tex', models.CharField(max_length=80, blank=True)),
                (b'the_geom', django.contrib.gis.db.models.fields.GeometryField(srid=3857)),
            ],
            options={
                'db_table': 'edigeo_subd_fisc',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name=b'EdigeoBati',
            fields=[
                (b'gid', models.IntegerField(serialize=False, primary_key=True)),
                (b'gb_ident', models.CharField(max_length=40, blank=True)),
                (b'gb_idnum', models.IntegerField(null=True, blank=True)),
                (b'dur', models.CharField(max_length=80, blank=True)),
                (b'the_geom', django.contrib.gis.db.models.fields.GeometryField(srid=3857)),
            ],
            options={
                'db_table': 'edigeo_bati',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name=b'EdigeoBorneParcel',
            fields=[
                (b'gid', models.IntegerField(serialize=False, primary_key=True)),
                (b'gb_ident', models.CharField(max_length=40, blank=True)),
                (b'gb_idnum', models.IntegerField(null=True, blank=True)),
                (b'the_geom', django.contrib.gis.db.models.fields.GeometryField(srid=3857)),
            ],
            options={
                'db_table': 'edigeo_borne_parcel',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name=b'EdigeoLieuDit',
            fields=[
                (b'gid', models.IntegerField(serialize=False, primary_key=True)),
                (b'gb_ident', models.CharField(max_length=40, blank=True)),
                (b'gb_idnum', models.IntegerField(null=True, blank=True)),
                (b'tex10', models.CharField(max_length=80, blank=True)),
                (b'tex2', models.CharField(max_length=80, blank=True)),
                (b'tex3', models.CharField(max_length=80, blank=True)),
                (b'tex4', models.CharField(max_length=80, blank=True)),
                (b'tex5', models.CharField(max_length=80, blank=True)),
                (b'tex6', models.CharField(max_length=80, blank=True)),
                (b'tex7', models.CharField(max_length=80, blank=True)),
                (b'tex8', models.CharField(max_length=80, blank=True)),
                (b'tex9', models.CharField(max_length=80, blank=True)),
                (b'tex', models.CharField(max_length=80, blank=True)),
                (b'the_geom', django.contrib.gis.db.models.fields.GeometryField(srid=3857)),
            ],
            options={
                'db_table': 'edigeo_lieu_dit',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name=b'EdigeoParcelle',
            fields=[
                (b'gid', models.IntegerField(serialize=False, primary_key=True)),
                (b'insee', models.ForeignKey(to=b'cad.Insee', to_field='id', null=True)),
                (b'gb_ident', models.CharField(max_length=40, blank=True)),
                (b'gb_idnum', models.IntegerField(null=True, blank=True)),
                (b'coar', models.CharField(max_length=1, blank=True)),
                (b'codm', models.CharField(max_length=80, blank=True)),
                (b'idu', models.CharField(max_length=20, blank=True)),
                (b'indp', models.CharField(max_length=80, blank=True)),
                (b'supf', models.DecimalField(null=True, max_digits=8, decimal_places=2, blank=True)),
                (b'tex2', models.CharField(max_length=80, blank=True)),
                (b'tex', models.CharField(max_length=80, blank=True)),
                (b'the_geom', django.contrib.gis.db.models.fields.GeometryField(srid=3857)),
            ],
            options={
                'db_table': 'edigeo_parcelle',
            },
            bases=(models.Model,),
        ),
    ]
