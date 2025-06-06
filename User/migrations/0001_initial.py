# Generated by Django 5.1.4 on 2025-02-07 14:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Guest', '0021_alter_tbl_renter_renter_status'),
        ('Renter', '0006_tbl_gallery'),
    ]

    operations = [
        migrations.CreateModel(
            name='tbl_cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart_quantity', models.CharField(max_length=50)),
                ('cart_status', models.IntegerField(default=0)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Renter.tbl_product')),
            ],
        ),
        migrations.CreateModel(
            name='tbl_complaint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('complaint_message', models.CharField(max_length=50)),
                ('complaint_status', models.CharField(choices=[('Pending', 'Pending'), ('Resolved', 'Resolved'), ('Closed', 'Closed')], default='Pending', max_length=255)),
                ('complaint_date', models.DateField(auto_now_add=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Renter.tbl_product')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Guest.tbl_user')),
            ],
        ),
        migrations.CreateModel(
            name='tbl_rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating_value', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])),
                ('rating_review', models.CharField(max_length=50)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Renter.tbl_product')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Guest.tbl_user')),
            ],
        ),
    ]
