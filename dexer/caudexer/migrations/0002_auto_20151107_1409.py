# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('caudexer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='caudexerbook',
            name='authors',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='caudexerbook',
            name='categories',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='caudexerbook',
            name='isbn_13',
            field=models.CharField(blank=True, max_length=300, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='goodreadsdata',
            name='timestamp',
            field=models.DateField(auto_now_add=True, default=datetime.datetime(2015, 11, 7, 14, 9, 36, 582454, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='googlebooksdata',
            name='categories',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='googlebooksdata',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='googlebooksdata',
            name='timestamp',
            field=models.DateField(auto_now_add=True, default=datetime.datetime(2015, 11, 7, 14, 9, 46, 79138, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='caudexerbook',
            unique_together=set([('isbn_13', 'title', 'authors')]),
        ),
    ]
