from django.db import models
from pet_welfare.models.vaccine import Vaccine
from pet_welfare.models.listing import Listing

class Vaccination(models.Model):
    listing = models.ForeignKey(
        Listing, 
        on_delete=models.CASCADE, 
        related_name="vaccinations"
    )
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE)
    date = models.DateField()

    class Meta:
        db_table = "vaccinations"
        unique_together = ("listing", "vaccine", "date")

    def clean(self):
        from django.core.exceptions import ValidationError
        
        if self.listing.listing_type != Listing.ADOPTION:
            raise ValidationError("Vaccinations can only be assigned to adoption listings.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
