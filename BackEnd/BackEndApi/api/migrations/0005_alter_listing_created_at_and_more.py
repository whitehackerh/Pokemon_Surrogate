# Generated by Django 4.2.1 on 2023-06-27 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_listing_listingnegotiations_listingpictures'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='listingnegotiations',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='listingpictures',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
