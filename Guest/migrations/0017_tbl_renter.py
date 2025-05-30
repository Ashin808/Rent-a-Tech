# Generated by Django 5.1.4 on 2025-02-06 10:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0012_tbl_staff'),
        ('Guest', '0016_remove_tbl_user_user_place'),
    ]

    operations = [
        migrations.CreateModel(
            name='tbl_renter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('renter_name', models.CharField(max_length=50)),
                ('renter_email', models.CharField(max_length=50)),
                ('renter_contact', models.CharField(max_length=50)),
                ('renter_address', models.CharField(max_length=50)),
                ('renter_password', models.CharField(max_length=50)),
                ('renter_type', models.IntegerField(default=0)),
                ('renter_logo', models.FileField(upload_to='Assets/Files/Renter')),
                ('renter_proof', models.FileField(upload_to='Assets/Files/Renter')),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Admin.tbl_place')),
            ],
        ),
    ]
