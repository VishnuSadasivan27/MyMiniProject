# Generated by Django 4.1.2 on 2023-02-27 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0009_alter_orderitem_totalproductcost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='totalproductcost',
            field=models.IntegerField(),
        ),
    ]