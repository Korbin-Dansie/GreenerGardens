# Generated by Django 4.2.5 on 2023-11-25 15:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gardens', '0004_alter_garden_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='garden',
            name='image_alt',
        ),
    ]
