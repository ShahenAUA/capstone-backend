# Generated by Django 5.1.7 on 2025-04-07 18:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pet_welfare', '0002_alter_profile_phone'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Vaccine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('manufacturer', models.CharField(blank=True, max_length=100, null=True)),
                ('protection_duration_months', models.IntegerField(default=12, help_text='How long the vaccine is effective (months)')),
            ],
            options={
                'db_table': 'vaccines',
            },
        ),
        migrations.AddField(
            model_name='profile',
            name='user_type',
            field=models.CharField(choices=[('individual', 'Individual'), ('shelter', 'Shelter')], default='individual', max_length=10),
        ),
        migrations.CreateModel(
            name='ShelterProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('address', models.TextField()),
                ('description', models.TextField(blank=True, null=True)),
                ('capacity', models.PositiveIntegerField(default=0)),
                ('registration_number', models.CharField(max_length=50, unique=True)),
                ('website', models.URLField(blank=True, null=True)),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='shelter_profile', to='pet_welfare.profile')),
            ],
            options={
                'db_table': 'shelter_profiles',
            },
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('type', models.CharField(choices=[('dog', 'Dog'), ('cat', 'Cat'), ('parrot', 'Parrot'), ('rabbit', 'Rabbit'), ('fish', 'Fish'), ('hamster', 'Hamster'), ('other', 'Other')], max_length=20)),
                ('breed', models.CharField(blank=True, max_length=100, null=True)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('weight', models.FloatField(blank=True, help_text='Weight in kg', null=True)),
                ('gender', models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female')], max_length=10, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('listing_type', models.CharField(choices=[('adoption', 'Adoption'), ('lost', 'Lost')], max_length=10)),
                ('listing_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(max_length=20)),
                ('last_seen_location', models.CharField(blank=True, max_length=255, null=True)),
                ('last_seen_date', models.DateField(blank=True, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='listings', to=settings.AUTH_USER_MODEL)),
                ('shelter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='listings', to='pet_welfare.shelterprofile')),
            ],
            options={
                'db_table': 'listings',
            },
        ),
        migrations.CreateModel(
            name='Vaccination',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vaccinations', to='pet_welfare.listing')),
                ('vaccine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pet_welfare.vaccine')),
            ],
            options={
                'db_table': 'vaccinations',
                'unique_together': {('listing', 'vaccine', 'date')},
            },
        ),
    ]
