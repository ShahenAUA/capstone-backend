from rest_framework import serializers
from pet_welfare.models import Listing, ListingBookmark
from mobile_api.utils import calculate_distance

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
            return calculate_distance(
                float(user_lat), float(user_lon),
                float(obj.last_seen_location_latitude), float(obj.last_seen_location_longitude)
            )
        return None
    
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
    is_bookmarked = serializers.SerializerMethodField()
    
    class Meta:
        model = Listing
        fields = [
            'id', 'name', 'age', 'type', 'breed', 'description', 'main_photo_url', 'is_vaccinated',
            'gender', 'weight', 'listing_date', 'contact_info', 'is_bookmarked'
        ]

    def get_age(self, obj):
        return obj.get_animal_age()

    def get_main_photo_url(self, obj):
        return obj.get_main_photo_url()
    
    def get_contact_info(self, obj):
        return ContactInfoSerializer(obj).data
    
    def get_is_bookmarked(self, obj):
        request = self.context.get('request')
        
        if request and request.user.is_authenticated:
            return ListingBookmark.objects.filter(user=request.user, listing=obj).exists()
        return False

class GetLostListingDetailsSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()
    distance_in_km = serializers.SerializerMethodField()
    main_photo_url = serializers.SerializerMethodField()
    contact_info = serializers.SerializerMethodField()

    class Meta:
        model = Listing
        fields = [
            'id', 'name', 'age', 'type', 'breed', 'description', 'distance_in_km', 'is_vaccinated', 'main_photo_url', 'last_seen_date',
            'gender', 'weight', 'last_seen_location_longitude', 'last_seen_location_latitude', 'last_seen_date', 'listing_date', 'contact_info'
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
            return calculate_distance(
                float(user_lat), float(user_lon),
                float(obj.last_seen_location_latitude), float(obj.last_seen_location_longitude)
            )
        return None
