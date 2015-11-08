# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caudexer', '0004_amazonbook'),
    ]

    operations = [
        migrations.AlterField(
            model_name='amazonbook',
            name='publication_date',
            field=models.DateField(null=True),
        ),
    ]
