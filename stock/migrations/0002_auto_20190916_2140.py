# Generated by Django 2.2.5 on 2019-09-16 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0001_initial'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='company',
            index=models.Index(fields=['quote'], name='quote_idx'),
        ),
    ]
