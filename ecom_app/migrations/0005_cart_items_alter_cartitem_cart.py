# Generated by Django 5.0.1 on 2024-02-05 05:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecom_app', '0004_remove_cartitem_user_alter_cart_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='items',
            field=models.ManyToManyField(related_name='cart_items', to='ecom_app.cartitem'),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='ecom_app.cart'),
        ),
    ]