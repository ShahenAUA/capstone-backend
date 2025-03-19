from django.db import models
from django.contrib.auth.models import User
from pet_welfare.models import Animal, ShelterProfile

class Listing(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name="listings")
    listing_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="listings")
    shelter = models.ForeignKey(ShelterProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name="listings")
    status = models.CharField(
        max_length=20,
        choices=[("available", "Available"), ("adopted", "Adopted"), ("pending", "Pending")],
        default="available",
    )

    class Meta:
        db_table = "listings"
