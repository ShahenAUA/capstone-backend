from django.urls import path, re_path

from .views import *
from .utils import schema_view

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('register_shelter', RegisterShelterView.as_view(), name='register-shelter'),
    path('verify', VerifyView.as_view(), name='verify'),
    path('login', LoginView.as_view(), name='login'),
    path('token-refresh', UserTokenRefreshView.as_view(), name='token-refresh'),
    
    path('password-reset', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password-reset/verify-code/<str:encoded_pk>', PasswordResetCodeVerifyView.as_view(), name='password-reset-code-verify'),
    path('password-reset-confirm/<str:encoded_pk>/<str:token>', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),

    path('species', UserGetMeView.as_view(), name='get-species'),
    # receive animal type (dog, cat, ...), return the respective array from json

    path('user/me', UserGetMeView.as_view(), name='user-me'),
    path('user/edit', UserGetMeView.as_view(), name='user-me'),
    # first, last name, shelter name, phone, profile picture
    # backlog, email, password if we manage

    path('user/listings/adoptions', GetListingsView.as_view(), name='get-listings-adoptions'),
    # add is_vaccinated to filters
    path('user/listings/adoptions/add', AddListingView.as_view(), name='add-listing-adoption'), # add validation for animal breed from json
    # multiple pictures, one main
    path('user/listings/lost', GetListingsView.as_view(), name='get-listings-lost'),
    # add is_vaccinated to filters, receive user longitude, latitude optionally, if defined sort by distance of last_seen location
    # return approximate distance radius field based on location
    path('user/listings/lost/add', AddListingView.as_view(), name='add-listing-lost'),
    # multiple pictures, one main

    path('user/listings/:id', GetListingsView.as_view(), name='get-listings-lost'),
    # return details of the listing, also add user/shelter information like name first name, contact phone, email

    path('user/listings/edit', AddListingView.as_view(), name='add-listing-lost'), # check by authorization
    # edit listing picture

    path('user/listings/adoptions', AddListingView.as_view(), name='add-listing-lost'), # created by user/shelter
    # return in the same serializer way
    path('user/listings/lost', AddListingView.as_view(), name='add-listing-lost'), # created by user/shelter
    # return in the same serializer way

    path('user/listings/bookmark', AddListingView.as_view(), name='add-listing-lost'),
    # receive listing_id, return only success message
    path('user/listings/get-bookmarks', AddListingView.as_view(), name='add-listing-lost'),
    # return same serialized version as adoption serializer

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json')
]

# priority
# 1 - image upload for listings
# 2 - listing endpoint separation
# 3 - update swagger (why pagination on user/me, fix filters, etc)
