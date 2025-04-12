from django.utils import timezone
from datetime import timedelta

def get_birth_date_for_age(age):
    return timezone.now().date() - timedelta(days=age * 365)
