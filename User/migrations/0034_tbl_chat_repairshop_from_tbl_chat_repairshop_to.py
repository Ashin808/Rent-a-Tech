# Generated by Django 5.1.7 on 2025-04-22 09:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Guest', '0026_tbl_repairshop'),
        ('User', '0033_tbl_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='tbl_chat',
            name='repairshop_from',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='repairshop_from', to='Guest.tbl_repairshop'),
        ),
        migrations.AddField(
            model_name='tbl_chat',
            name='repairshop_to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='repairshop_to', to='Guest.tbl_repairshop'),
        ),
    ]
