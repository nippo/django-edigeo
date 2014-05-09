# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('edigeo', '0004_auto_20140509_1047'),
    ]

    operations = [
        migrations.AddField(
            model_name='edigeoparcelle',
            name='section_idu',
            field=models.CharField(max_length=20, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='edigeoparcelle',
            name='commune_idu',
            field=models.CharField(max_length=20, null=True, blank=True),
            preserve_default=True,
        ),
    ]
