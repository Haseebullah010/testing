# Generated by Django 3.2.16 on 2022-10-29 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rasa_action', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Calendar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_date', models.CharField(max_length=14)),
            ],
            options={
                'db_table': 'Calendar',
            },
        ),
    ]
