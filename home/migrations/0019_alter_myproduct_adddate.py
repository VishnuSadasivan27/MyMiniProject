# Generated by Django 4.1.2 on 2023-03-29 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0018_remove_myproduct_review_review_product_review_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myproduct',
            name='adddate',
            field=models.DateField(auto_now_add=True),
        ),
    ]
