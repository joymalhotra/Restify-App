# Generated by Django 4.0.3 on 2022-03-06 01:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0001_initial'),
        ('accounts', '0002_alter_profile_phone_numer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='follows',
            field=models.ManyToManyField(blank=True, to='restaurants.restaurant'),
        ),
    ]
