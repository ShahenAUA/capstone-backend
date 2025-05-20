from rest_framework import serializers
from pet_welfare.models import Listing

class ListingFilterSerializer(serializers.Serializer):
    listing_type = serializers.ChoiceField(choices=Listing.LISTING_TYPE_CHOICES, required=False)
    
    type = serializers.ChoiceField(choices=Listing.ANIMAL_TYPE_CHOICES, required=False)
    breed = serializers.CharField(required=False)
    gender = serializers.ChoiceField(choices=Listing.GENDER_CHOICES, required=False)
    
    min_age = serializers.IntegerField(required=False, min_value=0)
    max_age = serializers.IntegerField(required=False, min_value=0)

    min_weight = serializers.FloatField(required=False, min_value=0)
    max_weight = serializers.FloatField(required=False, min_value=0)
    
    is_vaccinated = serializers.BooleanField(required=False)
    
    search = serializers.CharField(required=False, allow_blank=True)

class LostListingSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()
    distance_in_km = serializers.SerializerMethodField()
    main_photo_url = serializers.SerializerMethodField()

    class Meta:
        model = Listing
        fields = [
            'id', 'name', 'age', 'type', 'breed', 'description', 'distance_in_km', 'main_photo_url', 'last_seen_date'
        ]

    def get_age(self, obj):
        return obj.get_animal_age()

    def get_main_photo_url(self, obj):
        return obj.get_main_photo_url()
    
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
    
class ContactInfoSerializer(serializers.Serializer):
    full_name = serializers.CharField()
    email = serializers.EmailField()
    phone = serializers.CharField(required=False)
    is_shelter = serializers.BooleanField()
    address = serializers.CharField()
    website = serializers.CharField()

    def to_representation(self, instance):
        user = instance.shelter.user if instance.shelter else instance.user
        profile = getattr(user, "profile", None)
        
        result = {
            "full_name": f"{user.first_name} {user.last_name}".strip(),
            "email": user.email,
            "phone": profile.phone if profile else None,
            "is_shelter": profile.is_shelter() if profile else False,
            "address": profile.shelter_profile.address if profile.is_shelter() else None,
            "website": profile.shelter_profile.website if profile.is_shelter() else None,
        }
        
        return result

class GetAdoptionListingDetailsSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()
    main_photo_url = serializers.SerializerMethodField()
    contact_info = serializers.SerializerMethodField()
    
    class Meta:
        model = Listing
        fields = [
            'id', 'name', 'age', 'type', 'breed', 'description', 'main_photo_url', 'is_vaccinated',
            'gender', 'weight', 'listing_date', 'contact_info'
        ]

    def get_age(self, obj):
        return obj.get_animal_age()

    def get_main_photo_url(self, obj):
        return obj.get_main_photo_url()
    
    def get_contact_info(self, obj):
        return ContactInfoSerializer(obj).data

class GetLostListingDetailsSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()
    distance_in_km = serializers.SerializerMethodField()
    main_photo_url = serializers.SerializerMethodField()
    contact_info = serializers.SerializerMethodField()

    class Meta:
        model = Listing
        fields = [
            'id', 'name', 'age', 'type', 'breed', 'description', 'distance_in_km', 'is_vaccinated', 'main_photo_url', 'last_seen_date',
            'gender', 'weight', 'last_seen_location_longitude', 'last_seen_location_longitude', 'last_seen_date', 'listing_date', 'contact_info'
        ]

    def get_age(self, obj):
        return obj.get_animal_age()

    def get_main_photo_url(self, obj):
        return obj.get_main_photo_url()
    
    def get_contact_info(self, obj):
        return ContactInfoSerializer(obj).data
    
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
    