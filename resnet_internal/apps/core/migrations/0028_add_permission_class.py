# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-26 15:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_DATA_add_csd_domain_assign_to_navbar'),
    ]

    operations = [
        migrations.CreateModel(
            name='PermissionClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Class Name')),
                ('groups', models.ManyToManyField(related_name='permissionclasses', to='core.ADGroup', verbose_name='AD Groups')),
            ],
        ),
        migrations.AddField(
            model_name='navbarlink',
            name='permission_classes',
            field=models.ManyToManyField(to='core.PermissionClass', verbose_name='Permission Classes'),
        ),
        migrations.RemoveField(
            model_name='navbarlink',
            name='groups',
        ),
        migrations.AddField(
            model_name='navbarlink',
            name='show_to_all',
            field=models.BooleanField(default=False, verbose_name='Show To All Users'),
        ),
    ]
