from rest_framework import serializers
from pet_welfare.models import Listing
from mobile_api.messages import LONGITUDE_LATITUDE_SHOULD_BE_SET

class AddAdoptionListingSerializer(serializers.Serializer):
    name = serializers.CharField(required=False, allow_null=True, allow_blank=True, max_length=100)
    type = serializers.ChoiceField(choices=Listing.ANIMAL_TYPE_CHOICES)
    breed = serializers.CharField(required=False, allow_null=True, allow_blank=True, max_length=100)
    birth_date = serializers.DateField(required=False, allow_null=True)
    weight = serializers.FloatField(required=False, allow_null=True)
    gender = serializers.ChoiceField(choices=Listing.GENDER_CHOICES, required=False, allow_null=True)
    photo = serializers.ImageField(required=False)
    description = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    is_vaccinated = serializers.BooleanField(required=False, default=False)

class AddLostListingSerializer(serializers.Serializer):
    name = serializers.CharField(required=False, allow_null=True, allow_blank=True, max_length=100)
    type = serializers.ChoiceField(choices=Listing.ANIMAL_TYPE_CHOICES)
    breed = serializers.CharField(required=False, allow_null=True, allow_blank=True, max_length=100)
    birth_date = serializers.DateField(required=False, allow_null=True)
    weight = serializers.FloatField(required=False, allow_null=True)
    gender = serializers.ChoiceField(choices=Listing.GENDER_CHOICES, required=False, allow_null=True)
    photo = serializers.ImageField(required=False)
    description = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    is_vaccinated = serializers.BooleanField(required=False, default=False)

    last_seen_location_longitude = serializers.DecimalField(required=False, max_digits=9, decimal_places=6)
    last_seen_location_latitude = serializers.DecimalField(required=False, max_digits=9, decimal_places=6)
    last_seen_date = serializers.DateField(required=False, allow_null=True)

    def validate(self, data):
        longitude = data.get('last_seen_location_longitude')
        latitude = data.get('last_seen_location_latitude')

        if (longitude is not None and latitude is None) or (longitude is None and latitude is not None):
            raise serializers.ValidationError(LONGITUDE_LATITUDE_SHOULD_BE_SET)
        
        return data
    
class ListingListSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()
    main_photo_url = serializers.SerializerMethodField()

    class Meta:
        model = Listing
        fields = [
            'id', 'name', 'age', 'type', 'breed', 'description', 'main_photo_url'
        ]

    def get_age(self, obj):
        return obj.get_animal_age()

    def get_main_photo_url(self, obj):
        return obj.get_main_photo_url()
