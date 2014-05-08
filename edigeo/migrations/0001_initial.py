# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cad', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='EdigeoSection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('idu', models.CharField(unique=True, max_length=100)),
                ('tex', models.CharField(max_length=80, blank=True)),
                ('the_geom', django.contrib.gis.db.models.fields.GeometryField(srid=3857)),
            ],
            options={
                'db_table': 'edigeo_section',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EdigeoSubdFisc',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tex', models.CharField(max_length=80, blank=True)),
                ('md5', models.CharField(unique=True, max_length=80, blank=True)),
                ('the_geom', django.contrib.gis.db.models.fields.GeometryField(srid=3857)),
            ],
            options={
                'db_table': 'edigeo_subd_fisc',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EdigeoBati',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('the_geom', django.contrib.gis.db.models.fields.GeometryField(srid=3857)),
            ],
            options={
                'db_table': 'edigeo_bati',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EdigeoBorneParcel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('the_geom', django.contrib.gis.db.models.fields.GeometryField(srid=3857)),
            ],
            options={
                'db_table': 'edigeo_borne_parcel',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EdigeoLieuDit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tex', models.CharField(max_length=80, blank=True)),
                ('md5', models.CharField(unique=True, max_length=80, blank=True)),
                ('the_geom', django.contrib.gis.db.models.fields.GeometryField(srid=3857)),
            ],
            options={
                'db_table': 'edigeo_lieu_dit',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EdigeoParcelle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('insee', models.ForeignKey(to='cad.Insee', to_field='id', null=True)),
                ('idu', models.CharField(unique=True, max_length=20, blank=True)),
                ('supf', models.DecimalField(null=True, max_digits=8, decimal_places=2, blank=True)),
                ('tex', models.CharField(max_length=80, blank=True)),
                ('the_geom', django.contrib.gis.db.models.fields.GeometryField(srid=3857)),
            ],
            options={
                'db_table': 'edigeo_parcelle',
            },
            bases=(models.Model,),
        ),
    ]
