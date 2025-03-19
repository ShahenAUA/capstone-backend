from django.db import models

class Vaccine(models.Model):
    name = models.CharField(max_length=100, unique=True)
    manufacturer = models.CharField(max_length=100, blank=True, null=True)
    protection_duration_months = models.IntegerField(default=12, help_text="How long the vaccine is effective (months)")

    class Meta:
        db_table = "vaccines"
