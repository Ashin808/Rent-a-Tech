# Generated by Django 5.1.4 on 2025-02-14 09:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Guest', '0026_tbl_repairshop'),
        ('User', '0024_tbl_repair'),
    ]

    operations = [
        migrations.AddField(
            model_name='tbl_repair',
            name='repair',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Guest.tbl_repairshop'),
        ),
    ]
