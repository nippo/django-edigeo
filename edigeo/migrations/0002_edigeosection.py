# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('edigeo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EdigeoSection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('gb_ident', models.CharField(max_length=40, blank=True)),
                ('gb_idnum', models.CharField(max_length=40, null=True, blank=True)),
                ('idu', models.CharField(unique=True, max_length=100)),
                ('tex', models.CharField(max_length=80, blank=True)),
                ('the_geom', django.contrib.gis.db.models.fields.GeometryField(srid=3857)),
            ],
            options={
                'db_table': 'edigeo_section',
            },
            bases=(models.Model,),
        ),
    ]
