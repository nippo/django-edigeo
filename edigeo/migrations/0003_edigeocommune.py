# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('edigeo', '0002_remove_edigeoparcelle_insee'),
    ]

    operations = [
        migrations.CreateModel(
            name='EdigeoCommune',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('idu', models.CharField(unique=True, max_length=100)),
                ('gb_ident', models.CharField(max_length=80, blank=True)),
                ('the_geom', django.contrib.gis.db.models.fields.GeometryField(srid=3857)),
            ],
            options={
                'db_table': 'edigeo_commune',
            },
            bases=(models.Model,),
        ),
    ]
