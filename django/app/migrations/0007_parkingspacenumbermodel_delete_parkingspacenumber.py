# Generated by Django 4.2.1 on 2023-05-09 14:11

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_parkingspacenumber'),
    ]

    operations = [
        migrations.CreateModel(
            name='ParkingSpaceNumberModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(validators=[django.core.validators.MinValueValidator(limit_value=1)])),
                ('is_full', models.BooleanField(default=False)),
                ('row', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='numbers', to='app.parkingspacerowmodel')),
            ],
        ),
        migrations.DeleteModel(
            name='ParkingSpaceNumber',
        ),
    ]
