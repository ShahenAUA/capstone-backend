from django.db import models
from pet_welfare.models import Profile

class ShelterProfile(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name="shelter_profile")
    name = models.CharField(max_length=255)
    address = models.TextField()
    description = models.TextField(blank=True, null=True)
    capacity = models.PositiveIntegerField(default=0)
    registration_number = models.CharField(max_length=50, unique=True)
    website = models.URLField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        db_table = "shelter_profiles"
