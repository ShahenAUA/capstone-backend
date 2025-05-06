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
    description = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    is_vaccinated = serializers.BooleanField(required=False, default=False)

class AddLostListingSerializer(serializers.Serializer):
    name = serializers.CharField(required=False, allow_null=True, allow_blank=True, max_length=100)
    type = serializers.ChoiceField(choices=Listing.ANIMAL_TYPE_CHOICES)
    breed = serializers.CharField(required=False, allow_null=True, allow_blank=True, max_length=100)
    birth_date = serializers.DateField(required=False, allow_null=True)
    weight = serializers.FloatField(required=False, allow_null=True)
    gender = serializers.ChoiceField(choices=Listing.GENDER_CHOICES, required=False, allow_null=True)
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
    
class ListingFilterSerializer(serializers.Serializer):
    listing_type = serializers.ChoiceField(choices=Listing.LISTING_TYPE_CHOICES, required=False)
    
    type = serializers.ChoiceField(choices=Listing.ANIMAL_TYPE_CHOICES, required=False)
    breed = serializers.CharField(required=False)
    gender = serializers.ChoiceField(choices=Listing.GENDER_CHOICES, required=False)
    
    min_age = serializers.IntegerField(required=False, min_value=0)
    max_age = serializers.IntegerField(required=False, min_value=0)

    min_weight = serializers.FloatField(required=False, min_value=0)
    max_weight = serializers.FloatField(required=False, min_value=0)

class LostListingSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()
    distance_in_km = serializers.SerializerMethodField()

    class Meta:
        model = Listing
        fields = [
            'id', 'name', 'age', 'type', 'breed', 'description', 'distance_in_km' # first picture
        ]

    def get_age(self, obj):
        return obj.get_animal_age()
    
    def get_distance_in_km(self, obj):
        user_lat = self.context.get('user_latitude')
        user_lon = self.context.get('user_longitude')

        if (
            user_lat is not None and user_lon is not None and
            obj.last_seen_location_latitude is not None and obj.last_seen_location_longitude is not None
        ):
            return self._calculate_distance(
                float(user_lat), float(user_lon),
                float(obj.last_seen_location_latitude), float(obj.last_seen_location_longitude)
            )
        return None

    def _calculate_distance(self, lat1, lon1, lat2, lon2):
        from math import radians, sin, cos, sqrt, atan2

        # switch here to get different metrics
        R = 6371  # Earth radius in kilometers
        # R = 6371000  # Earth radius in meters

        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)
        a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = R * c
        return round(distance, 2)


class ListingListSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()

    class Meta:
        model = Listing
        fields = [
            'id', 'name', 'age', 'type', 'breed', 'description', # first picture
        ]
        # fields = [
        #     'id', 'name', 'type', 'breed', 'gender', 'birth_date',
        #     'weight', 'description', 'listing_type', 'status',
        #     'last_seen_location_longitude', 'last_seen_location_longitude', 'last_seen_date', 'listing_date', 'age'
        # ]

    def get_age(self, obj):
        return obj.get_animal_age()
