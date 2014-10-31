# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sharedlib', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='score',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='album',
            name='vote_count',
            field=models.IntegerField(default=0),
        ),
    ]
