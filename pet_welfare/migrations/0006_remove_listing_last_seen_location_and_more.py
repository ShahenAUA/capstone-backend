# Generated by Django 5.1.7 on 2025-05-06 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pet_welfare', '0005_alter_listing_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='last_seen_location',
        ),
        migrations.AddField(
            model_name='listing',
            name='is_vaccinated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='listing',
            name='last_seen_location_latitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='listing',
            name='last_seen_location_longitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('handled', 'Handled')], max_length=20),
        ),
        migrations.DeleteModel(
            name='Vaccination',
        ),
        migrations.DeleteModel(
            name='Vaccine',
        ),
    ]
