# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caudexer', '0003_auto_20151107_1415'),
    ]

    operations = [
        migrations.CreateModel(
            name='AmazonBook',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('price_and_currency', models.CharField(max_length=100)),
                ('asin', models.CharField(max_length=100)),
                ('sales_rank', models.IntegerField(null=True, blank=True)),
                ('offer_url', models.URLField(null=True, max_length=200, blank=True)),
                ('large_image_url', models.URLField(null=True, max_length=200, blank=True)),
                ('medium_image_url', models.URLField(null=True, max_length=200, blank=True)),
                ('small_image_url', models.URLField(null=True, max_length=200, blank=True)),
                ('authors', models.CharField(null=True, max_length=200, blank=True)),
                ('publisher', models.CharField(null=True, max_length=200, blank=True)),
                ('isbn_13', models.CharField(null=True, max_length=300, blank=True)),
                ('eisbn', models.CharField(null=True, max_length=300, blank=True)),
                ('binding', models.CharField(null=True, max_length=300, blank=True)),
                ('languages', models.CharField(null=True, max_length=300, blank=True)),
                ('edition', models.CharField(null=True, max_length=300, blank=True)),
                ('title', models.CharField(null=True, max_length=300, blank=True)),
                ('publication_date', models.DateField()),
                ('pages', models.IntegerField(null=True, blank=True)),
                ('caudexer_book', models.ForeignKey(to='caudexer.CaudexerBook')),
            ],
        ),
    ]
