# Generated by Django 4.2.1 on 2023-09-09 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_requests'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestPictures',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_id', models.IntegerField()),
                ('client_id', models.IntegerField()),
                ('path', models.CharField(max_length=255)),
                ('sort_no', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'request_pictures',
            },
        ),
    ]
