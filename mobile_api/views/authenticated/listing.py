from typing import Optional
from datetime import timedelta
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from pet_welfare.models import Listing, Profile, ShelterProfile
from mobile_api.utils import construct_response, construct_error, handle_validation_error, get_birth_date_for_age
from mobile_api.serializers import AddListingSerializer, ListingFilterSerializer, ListingListSerializer
from mobile_api.messages import UNKNOWN_ERROR, SHELTER_NOT_FOUND, LISTING_CREATED_SUCCESS, PROFILE_NOT_FOUND

class AddListingView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddListingSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)

            data = serializer.validated_data
            
            profile: Optional[Profile] = request.user.profile

            listing_kwargs = {
                'name': data.get('name'),
                'type': data['type'],
                'breed': data.get('breed'),
                'birth_date': data.get('birth_date'),
                'weight': data.get('weight'),
                'gender': data.get('gender'),
                'description': data.get('description'),
                'listing_type': data['listing_type'],
                'status': data['status'],
                'last_seen_location': data.get('last_seen_location'),
                'last_seen_date': data.get('last_seen_date'),
                'user': None,
                'shelter': None,
            }
            listing = Listing.objects.create(**listing_kwargs)

            if profile.is_shelter():
                shelter = profile.shelter_profile
                if not shelter:
                    return construct_error(message=SHELTER_NOT_FOUND, status=status.HTTP_400_BAD_REQUEST)
                listing.shelter = shelter
            else:
                listing.user = request.user

            listing.save()

            return construct_response(
                message=LISTING_CREATED_SUCCESS,
                data={'id': listing.id},
                status=status.HTTP_201_CREATED
            )
        except Profile.DoesNotExist:
            return construct_error(message=PROFILE_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return handle_validation_error(e)
        except Exception as e:
            print(e)
            return construct_error(message=UNKNOWN_ERROR, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetListingsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ListingListSerializer

    def get_queryset(self):
        params = ListingFilterSerializer(data=self.request.query_params)
        params.is_valid(raise_exception=True)
        data = params.validated_data

        queryset = Listing.objects.all()
        
        if 'listing_type' in data:
            queryset = queryset.filter(listing_type=data['listing_type'])
        
        if 'type' in data:
            queryset = queryset.filter(type=data['type'])
        if 'breed' in data:
            queryset = queryset.filter(breed__iexact=data['breed'])
        if 'gender' in data:
            queryset = queryset.filter(gender=data['gender'])
        if 'min_weight' in data:
            queryset = queryset.filter(weight__gte=data['min_weight'])
        if 'max_weight' in data:
            queryset = queryset.filter(weight__lte=data['max_weight'])        

        if 'min_age' in data:
            max_birth_date = get_birth_date_for_age(int(data['min_age']))
            queryset = queryset.filter(birth_date__lte=max_birth_date)
        if 'max_age' in data:
            min_birth_date = get_birth_date_for_age(int(data['max_age']))
            queryset = queryset.filter(birth_date__gte=min_birth_date)

        return queryset.order_by('-listing_date')

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.paginate_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            
            return construct_response(data=paginated_response.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return handle_validation_error(e)
        except Exception as e:
            print(e)
            return construct_error(message=UNKNOWN_ERROR, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
