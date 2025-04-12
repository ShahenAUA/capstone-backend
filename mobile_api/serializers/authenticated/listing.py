from rest_framework import serializers
from pet_welfare.models import Listing
from mobile_api.messages import INVALID_LISTING_TYPE

class AddListingSerializer(serializers.Serializer):
    name = serializers.CharField(required=False, allow_null=True, allow_blank=True, max_length=100)
    type = serializers.ChoiceField(choices=Listing.ANIMAL_TYPE_CHOICES)
    breed = serializers.CharField(required=False, allow_null=True, allow_blank=True, max_length=100)
    birth_date = serializers.DateField(required=False, allow_null=True)
    weight = serializers.FloatField(required=False, allow_null=True)
    gender = serializers.ChoiceField(choices=Listing.GENDER_CHOICES, required=False, allow_null=True)
    description = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    listing_type = serializers.ChoiceField(choices=Listing.LISTING_TYPE_CHOICES)
    
    last_seen_location = serializers.CharField(required=False, allow_null=True, allow_blank=True, max_length=255)
    last_seen_date = serializers.DateField(required=False, allow_null=True)

    def validate(self, attrs):
        listing_type = attrs.get('listing_type')

        if listing_type == Listing.ADOPTION:
            status=Listing.AVAILABLE
        elif listing_type == Listing.LOST:
            status=Listing.LOST
        else:
            raise serializers.ValidationError({'listing_type': INVALID_LISTING_TYPE})
        
        attrs['status'] = status
        return attrs

class ListingFilterSerializer(serializers.Serializer):
    listing_type = serializers.ChoiceField(choices=Listing.LISTING_TYPE_CHOICES, required=False)
    
    type = serializers.ChoiceField(choices=Listing.ANIMAL_TYPE_CHOICES, required=False)
    breed = serializers.CharField(required=False)
    gender = serializers.ChoiceField(choices=Listing.GENDER_CHOICES, required=False)
    
    min_age = serializers.IntegerField(required=False, min_value=0)
    max_age = serializers.IntegerField(required=False, min_value=0)

    min_weight = serializers.FloatField(required=False, min_value=0)
    max_weight = serializers.FloatField(required=False, min_value=0)

class ListingListSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()

    class Meta:
        model = Listing
        fields = [
            'id', 'name', 'type', 'breed', 'gender', 'birth_date',
            'weight', 'description', 'listing_type', 'status',
            'last_seen_location', 'last_seen_date', 'listing_date', 'age'
        ]

    def get_age(self, obj):
        return obj.get_animal_age()
