from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.db.models import Q
from django.http import Http404
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from pet_welfare.models import Listing
from mobile_api.utils import construct_response, construct_error, handle_validation_error, get_birth_date_for_age
from mobile_api.serializers import (ListingFilterSerializer, ListingListSerializer,
                                    LostListingSerializer, GetAdoptionListingDetailsSerializer, GetLostListingDetailsSerializer)
from mobile_api.messages import UNKNOWN_ERROR, ADOPTION_LISTING_NOT_FOUND, LOST_LISTING_NOT_FOUND

class GetAdoptionListingsView(generics.ListAPIView):
    permission_classes = [AllowAny,]
    serializer_class = ListingListSerializer
    authentication_classes=[]

    def get_queryset(self):
        params = ListingFilterSerializer(data=self.request.query_params)
        params.is_valid(raise_exception=True)
        data = params.validated_data
        queryset = Listing.objects.filter(listing_type=Listing.ADOPTION)

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
            
        if 'is_vaccinated' in data and data['is_vaccinated'] is not None:
            is_vaccinated = data['is_vaccinated']
            queryset = queryset.filter(is_vaccinated=is_vaccinated)

        print('search is: ', data.get('search'))

        if 'search' in data:
            search = data['search']
            print('filtering')
            queryset = queryset.filter(
                Q(name__icontains=search) | 
                Q(type__icontains=search) | 
                Q(breed__icontains=search)
            )
        
        return queryset.order_by('-listing_date')
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('type', openapi.IN_QUERY, description="Animal type", type=openapi.TYPE_STRING, enum=[choice[0] for choice in Listing.ANIMAL_TYPE_CHOICES]),
            openapi.Parameter('breed', openapi.IN_QUERY, description="Animal breed", type=openapi.TYPE_STRING),
            openapi.Parameter('gender', openapi.IN_QUERY, description="Animal gender", type=openapi.TYPE_STRING, enum=[choice[0] for choice in Listing.GENDER_CHOICES]),
            openapi.Parameter('min_age', openapi.IN_QUERY, description="Minimum age (in years)", type=openapi.TYPE_INTEGER),
            openapi.Parameter('max_age', openapi.IN_QUERY, description="Maximum age (in years)", type=openapi.TYPE_INTEGER),
            openapi.Parameter('min_weight', openapi.IN_QUERY, description="Minimum weight (kg)", type=openapi.TYPE_NUMBER, format='float'),
            openapi.Parameter('max_weight', openapi.IN_QUERY, description="Maximum weight (kg)", type=openapi.TYPE_NUMBER, format='float'),
            openapi.Parameter('search', openapi.IN_QUERY, description="Search listings based on name, type, breed", type=openapi.TYPE_STRING),
            openapi.Parameter('is_vaccinated', openapi.IN_QUERY, description="Vaccination status", type=openapi.TYPE_BOOLEAN),
        ],
    )
    def get(self, request, *args, **kwargs):
        try:
            queryset = self.paginate_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return construct_response(data=self.get_paginated_response(serializer.data).data)
        except ValidationError as e:
            return handle_validation_error(e)
        except Exception as e:
            print(e)
            return construct_error(message=UNKNOWN_ERROR, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetLostListingsView(GetAdoptionListingsView):
    permission_classes = [AllowAny,]
    serializer_class = LostListingSerializer
    authentication_classes=[]
    
    def get_queryset(self):
        params = ListingFilterSerializer(data=self.request.query_params)
        params.is_valid(raise_exception=True)
        data = params.validated_data
        queryset = Listing.objects.filter(listing_type=Listing.LOST)

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

        if 'is_vaccinated' in data and data['is_vaccinated'] is not None:
            is_vaccinated = data['is_vaccinated']
            queryset = queryset.filter(is_vaccinated=is_vaccinated)
            
        if 'search' in data:
            search = data['search']
            queryset = queryset.filter(
                Q(name__icontains=search) | 
                Q(type__icontains=search) | 
                Q(breed__icontains=search)
            )
            
        return queryset.order_by('-listing_date')

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('type', openapi.IN_QUERY, description="Animal type", type=openapi.TYPE_STRING, enum=[choice[0] for choice in Listing.ANIMAL_TYPE_CHOICES]),
            openapi.Parameter('breed', openapi.IN_QUERY, description="Animal breed", type=openapi.TYPE_STRING),
            openapi.Parameter('gender', openapi.IN_QUERY, description="Animal gender", type=openapi.TYPE_STRING, enum=[choice[0] for choice in Listing.GENDER_CHOICES]),
            openapi.Parameter('min_age', openapi.IN_QUERY, description="Minimum age (in years)", type=openapi.TYPE_INTEGER),
            openapi.Parameter('max_age', openapi.IN_QUERY, description="Maximum age (in years)", type=openapi.TYPE_INTEGER),
            openapi.Parameter('min_weight', openapi.IN_QUERY, description="Minimum weight (kg)", type=openapi.TYPE_NUMBER, format='float'),
            openapi.Parameter('max_weight', openapi.IN_QUERY, description="Maximum weight (kg)", type=openapi.TYPE_NUMBER, format='float'),
            openapi.Parameter('search', openapi.IN_QUERY, description="Search listings based on name, type, breed", type=openapi.TYPE_STRING),
            openapi.Parameter('is_vaccinated', openapi.IN_QUERY, description="Vaccination status", type=openapi.TYPE_BOOLEAN),
        ],
    )
    def get(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()

            user_lat = request.query_params.get('user_latitude')
            user_lon = request.query_params.get('user_longitude')

            try:
                user_lat = float(user_lat) if user_lat else None
                user_lon = float(user_lon) if user_lon else None
            except ValueError:
                return construct_error("Invalid latitude or longitude", status.HTTP_400_BAD_REQUEST)

            page = self.paginate_queryset(queryset)
            serializer_context = {
                'user_latitude': user_lat,
                'user_longitude': user_lon
            }

            if page is not None:
                serializer = LostListingSerializer(page, many=True, context=serializer_context)
                return self.get_paginated_response(serializer.data)

            serializer = LostListingSerializer(queryset, many=True, context=serializer_context)
            return construct_response(serializer.data)

        except ValidationError as e:
            return handle_validation_error(e)
        except Exception as e:
            return construct_error(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetAdoptionListingDetailsView(generics.RetrieveAPIView):
    serializer_class = GetAdoptionListingDetailsSerializer
    permission_classes = [AllowAny,]
    lookup_field = 'id'
    authentication_classes=[]

    def get_queryset(self):
        return Listing.objects.filter(listing_type=Listing.ADOPTION)

    @swagger_auto_schema(
        security=[{'Bearer': []}]
    )
    def get(self, request, *args, **kwargs):
        try:
            response = self.retrieve(request, *args, **kwargs)
            return construct_response(data=response.data)
        except Http404:
            return construct_error(message=ADOPTION_LISTING_NOT_FOUND, identifier='id', status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return construct_error(message=UNKNOWN_ERROR, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetLostListingDetailsView(generics.RetrieveAPIView):
    serializer_class = GetLostListingDetailsSerializer
    permission_classes = [AllowAny,]
    lookup_field = 'id'
    authentication_classes=[]

    def get_queryset(self):
        return Listing.objects.filter(listing_type=Listing.LOST)

    @swagger_auto_schema(
        security=[{'Bearer': []}]
    )
    def get(self, request, *args, **kwargs):
        try:
            response = self.retrieve(request, *args, **kwargs)
            return construct_response(data=response.data)
        except Http404:
            return construct_error(message=LOST_LISTING_NOT_FOUND, identifier='id', status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return construct_error(message=UNKNOWN_ERROR, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
