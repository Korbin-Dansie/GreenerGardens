# Generated by Django 4.2.5 on 2023-11-25 22:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gardens', '0007_alter_garden_section_garden_plant_category_plant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plant',
            name='category',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='gardens.plant_category'),
        ),
    ]
