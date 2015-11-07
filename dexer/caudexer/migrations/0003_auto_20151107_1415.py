# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caudexer', '0002_auto_20151107_1409'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goodreadsdata',
            name='good_reads_id',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='googlebooksdata',
            name='google_book_id',
            field=models.CharField(max_length=100),
        ),
    ]
