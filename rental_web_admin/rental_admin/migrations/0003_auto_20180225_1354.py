# Generated by Django 2.0.2 on 2018-02-25 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental_admin', '0002_auto_20180225_1321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crawlerconfig',
            name='filter_city',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='crawlerconfig',
            name='filter_neighborhood',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='crawlerconfig',
            name='filter_price',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='crawlerconfig',
            name='filter_square_meters',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
