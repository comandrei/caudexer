# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CaudexerBook',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(max_length=300, blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='GoodReadsData',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('good_reads_id', models.IntegerField()),
                ('average_rating', models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=4)),
                ('nr_reviews', models.IntegerField(blank=True, null=True)),
                ('nr_text_reviews', models.IntegerField(blank=True, null=True)),
                ('pub_year', models.IntegerField(blank=True, null=True)),
                ('pub_month', models.IntegerField(blank=True, null=True)),
                ('pub_day', models.IntegerField(blank=True, null=True)),
                ('title', models.CharField(max_length=300, blank=True, null=True)),
                ('authors', models.CharField(max_length=300, blank=True, null=True)),
                ('author_id', models.IntegerField()),
                ('small_img', models.CharField(max_length=300, blank=True, null=True)),
                ('img', models.CharField(max_length=300, blank=True, null=True)),
                ('caudexer_book', models.ForeignKey(to='caudexer.CaudexerBook')),
            ],
        ),
        migrations.CreateModel(
            name='GoogleBooksData',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('google_book_id', models.IntegerField()),
                ('title', models.CharField(max_length=300, blank=True, null=True)),
                ('snippet', models.TextField(blank=True, null=True)),
                ('authors', models.CharField(max_length=300, blank=True, null=True)),
                ('small_img', models.CharField(max_length=300, blank=True, null=True)),
                ('img', models.CharField(max_length=300, blank=True, null=True)),
                ('isbn_13', models.CharField(max_length=300, blank=True, null=True)),
                ('average_rating', models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=4)),
                ('nr_reviews', models.IntegerField(blank=True, null=True)),
                ('language', models.CharField(max_length=300, blank=True, null=True)),
                ('page_count', models.IntegerField(blank=True, null=True)),
                ('publish_year', models.IntegerField(blank=True, null=True)),
                ('caudexer_book', models.ForeignKey(to='caudexer.CaudexerBook')),
            ],
        ),
    ]
