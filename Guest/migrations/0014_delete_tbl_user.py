# Generated by Django 5.1.4 on 2025-01-25 10:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Guest', '0013_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='tbl_user',
        ),
    ]
