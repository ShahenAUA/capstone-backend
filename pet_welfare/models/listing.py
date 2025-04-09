from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from pet_welfare.models.shelter_profile import ShelterProfile

class Listing(models.Model):
    ADOPTION = "adoption"
    LOST = "lost"

    LISTING_TYPE_CHOICES = [
        (ADOPTION, "Adoption"),
        (LOST, "Lost"),
    ]

    ADOPTION_STATUSES = [
        ("available", "Available"),
        ("adopted", "Adopted"),
    ]

    LOST_STATUSES = [
        ("lost", "Lost"),
        ("reunited", "Reunited"),
    ]

    DOG = "dog"
    CAT = "cat"
    PARROT = "parrot"
    RABBIT = "rabbit"
    FISH = "fish"
    HAMSTER = "hamster"
    OTHER = "other"

    ANIMAL_TYPE_CHOICES = [
        (DOG, "Dog"),
        (CAT, "Cat"),
        (PARROT, "Parrot"),
        (RABBIT, "Rabbit"),
        (FISH, "Fish"),
        (HAMSTER, "Hamster"),
        (OTHER, "Other"),
    ]
    MALE = "male"
    FEMALE = "female"

    GENDER_CHOICES = [
        (MALE, "Male"),
        (FEMALE, "Female"),
    ]
    
    name = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=20, choices=ANIMAL_TYPE_CHOICES)
    breed = models.CharField(max_length=100, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True, help_text="Weight in kg")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    listing_type = models.CharField(max_length=10, choices=LISTING_TYPE_CHOICES)
    listing_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="listings")
    shelter = models.ForeignKey(ShelterProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name="listings")

    status = models.CharField(max_length=20)

    last_seen_location = models.CharField(max_length=255, blank=True, null=True)
    last_seen_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = "listings"

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.listing_type == self.ADOPTION and self.status not in dict(self.ADOPTION_STATUSES):
            raise ValidationError({"status": "Invalid status for an adoption listing."})
        elif self.listing_type == self.LOST and self.status not in dict(self.LOST_STATUSES):
            raise ValidationError({"status": "Invalid status for a lost listing."})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def get_animal_age(self):
        if self.birth_date:
            return (timezone.now().date() - self.birth_date).days // 365
        return None
    