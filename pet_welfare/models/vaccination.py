from django.db import models
from pet_welfare.models import Animal, Vaccine

class Vaccination(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name="vaccinations")
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE)
    date = models.DateField()

    class Meta:
        db_table = "vaccinations"
        unique_together = ("animal", "vaccine", "date")
