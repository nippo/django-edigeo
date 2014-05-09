# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('edigeo', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='edigeoparcelle',
            name='insee',
        ),
    ]
