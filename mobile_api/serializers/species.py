from rest_framework import serializers
from pet_welfare.models import Listing

class GetSpeciesByTypeSerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=Listing.ANIMAL_TYPE_CHOICES)
