# Generated by Django 4.0.3 on 2024-08-06 15:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0007_order_paid_order_payment_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='additional_info',
        ),
    ]
