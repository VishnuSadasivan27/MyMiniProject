# Generated by Django 4.1.2 on 2023-03-21 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_alter_registration_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='image',
            field=models.ImageField(upload_to='userimage/'),
        ),
    ]
