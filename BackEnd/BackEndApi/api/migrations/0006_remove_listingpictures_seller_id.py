# Generated by Django 4.2.1 on 2023-06-29 14:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_listing_created_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listingpictures',
            name='seller_id',
        ),
    ]
