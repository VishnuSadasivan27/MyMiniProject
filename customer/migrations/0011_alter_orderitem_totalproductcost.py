# Generated by Django 4.1.2 on 2023-02-27 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0010_alter_orderitem_totalproductcost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='totalproductcost',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]