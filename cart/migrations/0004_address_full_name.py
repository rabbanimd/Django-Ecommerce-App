# Generated by Django 3.1.7 on 2021-04-18 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_auto_20210418_1219'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='full_name',
            field=models.CharField(default=True, max_length=30),
        ),
    ]