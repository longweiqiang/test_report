# Generated by Django 2.1 on 2018-11-12 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commit', '0002_report_create_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='create_user',
            field=models.IntegerField(verbose_name='创建人'),
        ),
    ]
