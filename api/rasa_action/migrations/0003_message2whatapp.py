# Generated by Django 3.2.16 on 2022-10-30 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rasa_action', '0002_calendar'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message2WhatApp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('to_number', models.CharField(max_length=14)),
                ('message', models.CharField(max_length=1024)),
            ],
            options={
                'db_table': 'Message2WhatApp',
            },
        ),
    ]
