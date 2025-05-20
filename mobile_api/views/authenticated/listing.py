from typing import Optional
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from pet_welfare.models import Listing, Profile, ListingPhoto
from mobile_api.utils import construct_response, construct_error, handle_validation_error, process_uploaded_image
from mobile_api.serializers import (AddAdoptionListingSerializer, AddLostListingSerializer, ListingListSerializer)
from mobile_api.messages import UNKNOWN_ERROR, SHELTER_NOT_FOUND, LISTING_CREATED_SUCCESS, PROFILE_NOT_FOUND

class AddAdoptionListingView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddAdoptionListingSerializer
    parser_classes = [MultiPartParser]
    
    @swagger_auto_schema(
        request_body=AddAdoptionListingSerializer,
        responses={
            201: openapi.Response(
                description="Listing created successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER)
                    }
                )
            ),
            400: openapi.Response(description="Invalid input"),
            500: openapi.Response(description="Internal server error")
        },
        manual_parameters=[
            openapi.Parameter(
                'photo', 
                openapi.IN_FORM, 
                description="Photo of the pet", 
                type=openapi.TYPE_FILE
            )
        ]
    )
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
            profile: Optional[Profile] = request.user.profile

            listing = Listing.objects.create(
                name=data.get('name'),
                type=data['type'],
                breed=data.get('breed'),
                birth_date=data.get('birth_date'),
                weight=data.get('weight'),
                gender=data.get('gender'),
                description=data.get('description'),
                listing_type=Listing.ADOPTION,
                status=Listing.PENDING,
                user=request.user,
                shelter=None,
            )
            
            if profile.is_shelter():
                shelter = profile.shelter_profile
                if not shelter:
                    return construct_error(message=SHELTER_NOT_FOUND, status=status.HTTP_400_BAD_REQUEST)
                listing.shelter = shelter

            listing.save()
            
            photo_file = request.FILES.get('photo')
            if photo_file:
                adjusted_image = process_uploaded_image(
                    instance=listing,
                    image_field_name="photo",
                    image=photo_file,
                    prefix="listing"
                )
                ListingPhoto.objects.create(
                    listing=listing,
                    image=adjusted_image,
                    is_main=True
                )
                
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

class AddLostListingView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddLostListingSerializer
    parser_classes = [MultiPartParser]
    
    @swagger_auto_schema(
        request_body=AddLostListingSerializer,
        responses={
            201: openapi.Response(
                description="Listing created successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER)
                    }
                )
            ),
            400: openapi.Response(description="Invalid input"),
            500: openapi.Response(description="Internal server error")
        }
    )
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
            profile: Optional[Profile] = request.user.profile

            listing = Listing.objects.create(
                name=data.get('name'),
                type=data['type'],
                breed=data.get('breed'),
                birth_date=data.get('birth_date'),
                weight=data.get('weight'),
                gender=data.get('gender'),
                description=data.get('description'),
                listing_type=Listing.LOST,
                status=Listing.PENDING,
                last_seen_location_longitude=data.get('last_seen_location_longitude'),
                last_seen_location_latitude=data.get('last_seen_location_latitude'),
                last_seen_date=data.get('last_seen_date'),
                user=request.user,
                shelter=None,
            )
            
            if profile.is_shelter():
                shelter = profile.shelter_profile
                if not shelter:
                    return construct_error(message=SHELTER_NOT_FOUND, status=status.HTTP_400_BAD_REQUEST)
                listing.shelter = shelter

            listing.save()
            
            photo_file = request.FILES.get('photo')
            if photo_file:
                adjusted_image = process_uploaded_image(
                    instance=listing,
                    image_field_name="photo",
                    image=photo_file,
                    prefix="listing"
                )
                ListingPhoto.objects.create(
                    listing=listing,
                    image=adjusted_image,
                    is_main=True
                )
                
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
        
class GetMyAdoptionListingsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = ListingListSerializer

    def get_queryset(self):
        user = self.request.user
        # params = ListingFilterSerializer(data=self.request.query_params)
        # params.is_valid(raise_exception=True)
        # data = params.validated_data
        queryset = Listing.objects.filter(listing_type=Listing.ADOPTION, user=user)

        # if 'search' in data:
        #     queryset = queryset.filter()

        return queryset.order_by('-listing_date')

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.paginate_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return construct_response(data=self.get_paginated_response(serializer.data).data)
        except ValidationError as e:
            return handle_validation_error(e)
        except Exception as e:
            print(e)
            return construct_error(message=UNKNOWN_ERROR, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetMyLostListingsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = ListingListSerializer

    def get_queryset(self):
        user = self.request.user
        # params = ListingFilterSerializer(data=self.request.query_params)
        # params.is_valid(raise_exception=True)
        # data = params.validated_data
        queryset = Listing.objects.filter(listing_type=Listing.LOST, user=user)

        # if 'search' in data:
        #     queryset = queryset.filter()

        return queryset.order_by('-listing_date')

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.paginate_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return construct_response(data=self.get_paginated_response(serializer.data).data)
        except ValidationError as e:
            return handle_validation_error(e)
        except Exception as e:
            print(e)
            return construct_error(message=UNKNOWN_ERROR, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
