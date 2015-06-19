# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_confirmed_registration'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(upload_to=users.models.get_avatar_fn, verbose_name='avatar', blank=True),
            preserve_default=True,
        ),
    ]
