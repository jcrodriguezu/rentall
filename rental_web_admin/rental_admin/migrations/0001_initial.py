# Generated by Django 2.0.2 on 2018-02-18 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CrawlerConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('domain', models.CharField(max_length=200)),
                ('start_url', models.URLField()),
                ('pagination_regex', models.CharField(max_length=200)),
                ('xpath_item_list', models.CharField(max_length=200)),
                ('xpath_neighborhood', models.CharField(max_length=200)),
                ('xpath_square_meters', models.CharField(max_length=200)),
                ('xpath_price', models.CharField(max_length=200)),
                ('xpath_url', models.CharField(max_length=200)),
                ('xpath_detail', models.CharField(max_length=200)),
                ('xpath_title', models.CharField(max_length=200)),
                ('xpath_code', models.CharField(max_length=200)),
                ('xpath_next', models.CharField(max_length=200)),
            ],
        ),
    ]
