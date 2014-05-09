# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('edigeo', '0003_edigeocommune'),
    ]

    operations = [
        migrations.AlterField(
            model_name='edigeocommune',
            name='gb_ident',
            field=models.CharField(unique=True, max_length=80, blank=True),
        ),
    ]
