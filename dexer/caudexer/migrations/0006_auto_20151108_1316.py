# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caudexer', '0005_auto_20151108_1047'),
    ]

    operations = [
        migrations.AddField(
            model_name='amazonbook',
            name='average_rating',
            field=models.DecimalField(null=True, decimal_places=4, blank=True, max_digits=10),
        ),
        migrations.AddField(
            model_name='amazonbook',
            name='nr_reviews',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
