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

    # TODO - maybe join these types into available/handled
    PENDING = "pending"
    HANDLED = "handled"
    LISTING_STATUS_CHOICES = [
        (PENDING, "Pending"),
        (HANDLED, "Handled"),
    ]

    DOG = "dog"
    CAT = "cat"
    PARROT = "parrot"
    TURTLE = "turtle"
    RABBIT = "rabbit"
    FISH = "fish"
    HAMSTER = "hamster"
    OTHER = "other"

    ANIMAL_TYPE_CHOICES = [
        (DOG, "Dog"),
        (CAT, "Cat"),
        (PARROT, "Parrot"),
        (TURTLE, "Turtle"),
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
    is_vaccinated = models.BooleanField(default=False)
    listing_type = models.CharField(max_length=10, choices=LISTING_TYPE_CHOICES)
    listing_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="listings")
    shelter = models.ForeignKey(ShelterProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name="listings")

    status = models.CharField(max_length=20, choices=LISTING_STATUS_CHOICES)

    last_seen_location_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    last_seen_location_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    last_seen_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = "listings"

    def get_animal_age(self):
        if self.birth_date:
            return (timezone.now().date() - self.birth_date).days // 365
        return None
    