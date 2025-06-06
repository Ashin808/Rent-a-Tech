# Generated by Django 5.1.7 on 2025-03-16 21:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Guest', '0026_tbl_repairshop'),
        ('Renter', '0009_tbl_gallery'),
        ('User', '0032_delete_tbl_rating'),
    ]

    operations = [
        migrations.CreateModel(
            name='tbl_rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating_data', models.IntegerField()),
                ('user_review', models.CharField(max_length=500)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Renter.tbl_product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Guest.tbl_user')),
            ],
        ),
    ]
