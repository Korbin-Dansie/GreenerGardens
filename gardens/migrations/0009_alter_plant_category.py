# Generated by Django 4.2.5 on 2023-11-25 22:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gardens', '0008_alter_plant_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plant',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gardens.plant_category'),
        ),
    ]
