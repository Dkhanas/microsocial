# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(unique=True, max_length=75, verbose_name=b'email')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('sex', models.SmallIntegerField(default=0, verbose_name='\u0441\u0442\u0430\u0442\u044c', choices=[(0, '------'), (1, '\u0447\u043e\u043b\u043e\u0432\u0456\u0447\u0430'), (2, '\u0436\u0456\u043d\u043e\u0447\u0430')])),
                ('birth_date', models.DateField(null=True, verbose_name='\u0434\u0430\u0442\u0430 \u043d\u0430\u0440\u043e\u0434\u0436\u0435\u043d\u043d\u044f', blank=True)),
                ('city', models.CharField(max_length=50, verbose_name='\u043c\u0456\u0441\u0442\u043e', blank=True)),
                ('job', models.CharField(max_length=200, verbose_name='\u043c\u0456\u0441\u0446\u0435 \u0440\u043e\u0431\u043e\u0442\u0438', blank=True)),
                ('about_me', models.TextField(max_length=1000, verbose_name='\u043f\u0440\u043e \u0441\u0435\u0431\u0435', blank=True)),
                ('interests', models.TextField(max_length=1000, verbose_name='\u0456\u043d\u0442\u0435\u0440\u0435\u0441\u0438', blank=True)),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
