# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('videomain', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='videomainpage',
            name='checked',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='videomainpage',
            name='last_active',
            field=models.DateTimeField(default=django.utils.timezone.now, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='videomainpage',
            name='video_url',
            field=models.URLField(),
        ),
    ]
