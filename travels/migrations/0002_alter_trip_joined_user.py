# Generated by Django 3.2.6 on 2021-09-27 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travels', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='joined_user',
            field=models.ManyToManyField(blank=True, null=True, related_name='join_users', to='travels.User'),
        ),
    ]