# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=50, choices=[(b'wall_post', '\u043f\u043e\u0432\u0456\u0434\u043e\u043c\u043b\u0435\u043d\u043d\u044f \u043d\u0430 \u0441\u0442\u0456\u043d\u0456'), (b'make_friends', '\u0442\u0435\u043f\u0435\u0440 \u0434\u0440\u0443\u0437\u0456'), (b'break_friends', '\u0440\u043e\u0437\u0456\u0440\u0432\u0430\u043b\u0438 \u0434\u0440\u0443\u0436\u0431\u0443')])),
                ('object_id', models.PositiveIntegerField(null=True, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('content_type', models.ForeignKey(blank=True, to='contenttypes.ContentType', null=True)),
                ('target', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created',),
            },
            bases=(models.Model,),
        ),
    ]
