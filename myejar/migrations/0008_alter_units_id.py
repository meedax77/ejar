# Generated by Django 4.2.6 on 2024-01-16 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myejar', '0007_alter_units_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='units',
            name='id',
            field=models.BigAutoField(default='5542', primary_key=True, serialize=False),
        ),
    ]
