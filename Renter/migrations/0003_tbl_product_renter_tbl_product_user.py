# Generated by Django 5.1.4 on 2025-02-07 06:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Guest', '0021_alter_tbl_renter_renter_status'),
        ('Renter', '0002_tbl_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='tbl_product',
            name='renter',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Guest.tbl_renter'),
        ),
        migrations.AddField(
            model_name='tbl_product',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Guest.tbl_user'),
        ),
    ]
