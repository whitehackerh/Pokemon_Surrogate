# Generated by Django 4.2.1 on 2023-09-09 15:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_requestpictures'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='requests',
            name='fee_id',
        ),
    ]
