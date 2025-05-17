from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics
from pet_welfare.models import Listing, ListingBookmark
from mobile_api.utils import construct_error, construct_response, handle_validation_error
from mobile_api.serializers import ListingListSerializer
from mobile_api.messages import (UNKNOWN_ERROR, LISTING_ID_REQUIRED, BOOKMARKED_SUCCESSFULLY, ALREADY_BOOKMARKED, ADOPTION_LISTING_NOT_FOUND,
                                 BOOKMARK_REMOVED_SUCCESSFULLY, BOOKMARK_NOT_FOUND, CANNOT_BOOKMARK_YOUR_LISTING)

class AddListingBookmarkView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['listing_id'],
            properties={
                'listing_id': openapi.Schema(type=openapi.TYPE_INTEGER)
            }
        ),
    )
    def post(self, request):
        try:
            listing_id = request.data.get('listing_id')
            if not listing_id:
                return construct_error(LISTING_ID_REQUIRED, status=status.HTTP_400_BAD_REQUEST)

            try:
                listing = Listing.objects.get(id=listing_id, listing_type=Listing.ADOPTION) # only adoptions can be bookmarked
            except Listing.DoesNotExist:
                return construct_error(ADOPTION_LISTING_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)

            if listing.user == request.user:
                return construct_response(CANNOT_BOOKMARK_YOUR_LISTING, status=status.HTTP_400_BAD_REQUEST)
            
            bookmark, created = ListingBookmark.objects.get_or_create(user=request.user, listing=listing)
            if created:
                return construct_response(BOOKMARKED_SUCCESSFULLY, status=status.HTTP_201_CREATED)
            else:
                return construct_response(ALREADY_BOOKMARKED, status=status.HTTP_200_OK)
        except ValidationError as e:
            return handle_validation_error(e)
        except Exception as e:
            print(e)
            return construct_error(UNKNOWN_ERROR, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RemoveListingBookmarkView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['listing_id'],
            properties={
                'listing_id': openapi.Schema(type=openapi.TYPE_INTEGER)
            }
        ),
    )
    def post(self, request):
        try:
            listing_id = request.data.get('listing_id')
            if not listing_id:
                return construct_error(LISTING_ID_REQUIRED, status=status.HTTP_400_BAD_REQUEST)

            try:
                bookmark = ListingBookmark.objects.get(user=request.user, listing_id=listing_id)
                bookmark.delete()
                return construct_response(BOOKMARK_REMOVED_SUCCESSFULLY, status=status.HTTP_200_OK)
            except ListingBookmark.DoesNotExist:
                return construct_error(BOOKMARK_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return handle_validation_error(e)
        except Exception as e:
            print(e)
            return construct_error(UNKNOWN_ERROR, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetBookmarkedListingsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ListingListSerializer

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="Paginated list of bookmarked listings",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'count': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'next': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI, nullable=True),
                        'previous': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI, nullable=True),
                        'results': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_OBJECT)
                        )
                    }
                )
            ),
            500: openapi.Response(description="Internal server error")
        }
    )
    def list(self, request, *args, **kwargs):
        try:
            queryset = Listing.objects.filter(bookmarks__user=request.user).order_by('-listing_date')
            page = self.paginate_queryset(queryset)
            serializer = self.get_serializer(page, many=True)
            return construct_response(data=self.get_paginated_response(serializer.data).data)
        except Exception as e:
            print(e)
            return construct_error(message=UNKNOWN_ERROR, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
