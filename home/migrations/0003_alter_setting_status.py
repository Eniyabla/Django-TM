# Generated by Django 4.1 on 2022-08-27 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_setting'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setting',
            name='status',
            field=models.BooleanField(),
        ),
    ]