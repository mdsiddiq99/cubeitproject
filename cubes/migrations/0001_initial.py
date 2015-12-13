# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('contents', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cube',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='CubeContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.ForeignKey(to='contents.Content')),
                ('cube', models.ForeignKey(to='cubes.Cube')),
            ],
        ),
        migrations.CreateModel(
            name='UserCube',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cube', models.ForeignKey(to='cubes.Cube')),
                ('user', models.ForeignKey(to='users.UserProfile')),
            ],
        ),
    ]
