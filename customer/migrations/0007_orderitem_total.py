# Generated by Django 4.1.2 on 2023-02-27 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0006_order_myorder'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='total',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]