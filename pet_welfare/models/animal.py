# from django.db import models
# from django.utils import timezone
# from pet_welfare.models.shelter_profile import ShelterProfile

# class Animal(models.Model):
#     DOG = "dog"
#     CAT = "cat"
#     PARROT = "parrot"
#     RABBIT = "rabbit"
#     FISH = "fish"
#     HAMSTER = "hamster"
#     OTHER = "other"

#     TYPE_CHOICES = [
#         (DOG, "Dog"),
#         (CAT, "Cat"),
#         (PARROT, "Parrot"),
#         (RABBIT, "Rabbit"),
#         (FISH, "Fish"),
#         (HAMSTER, "Hamster"),
#         (OTHER, "Other"),
#     ]
#     MALE = "male"
#     FEMALE = "female"

#     GENDER_CHOICES = [
#         (MALE, "Male"),
#         (FEMALE, "Female"),
#     ]

#     type = models.CharField(max_length=20, choices=TYPE_CHOICES)
#     breed = models.CharField(max_length=100)
#     birth_date = models.DateField(null=True, blank=True)
#     weight = models.FloatField(null=True, blank=True, help_text="Weight in kg")
#     gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
#     name = models.CharField(max_length=100, blank=True, null=True)
#     description = models.TextField(blank=True, null=True)
#     shelter = models.ForeignKey(ShelterProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name="animals")

#     def age(self):
#         if self.birth_date:
#             return (timezone.now().date() - self.birth_date).days // 365
#         return None

#     class Meta:
#         db_table = "animals"
