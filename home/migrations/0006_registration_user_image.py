# Generated by Django 4.1.2 on 2023-03-09 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_alter_myproduct_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='user_image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
