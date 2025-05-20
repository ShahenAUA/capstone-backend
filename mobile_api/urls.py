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

    path('species', GetSpeciesView.as_view(), name='get-species'),

    path('user/me', UserGetMeView.as_view(), name='user-me'),
    # path('user/edit', UserGetMeView.as_view(), name='user-me'),
    
    # first, last name, shelter name, phone, profile picture
    # backlog, email, password if we manage
    
    path('user/listings/adoptions', GetAdoptionListingsView.as_view(), name='get-listings-adoptions'),
    path('user/listings/lost', GetLostListingsView.as_view(), name='get-listings-lost'),

    # add validation for animal breed from json
    path('user/listings/adoptions/add', AddAdoptionListingView.as_view(), name='add-listing-adoption'),
    path('user/listings/lost/add', AddLostListingView.as_view(), name='add-listing-lost'),
    
    path('user/listings/delete/<int:id>', DeleteListingView.as_view(), name='delete-listing'),

    path('user/listings/adoptions/<int:id>', GetAdoptionListingDetailsView.as_view(), name='get-listing-detail-adoption'),
    path('user/listings/lost/<int:id>', GetLostListingDetailsView.as_view(), name='get-listing-detail-lost'),

    # path('user/listings/edit', AddListingView.as_view(), name='add-listing-lost'), # check by authorization
    # edit listing picture

    path('user/listings/adoptions/my', GetMyAdoptionListingsView.as_view(), name='add-listing-lost'),
    path('user/listings/lost/my', GetMyLostListingsView.as_view(), name='add-listing-lost'),

    path('user/listings/bookmark', AddListingBookmarkView.as_view(), name='bookmark-listing'),
    path('user/listings/unmark', RemoveListingBookmarkView.as_view(), name='unmark-listing'),
    path('user/listings/get-bookmarks', GetBookmarkedListingsView.as_view(), name='get-bookmarked-listings'),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json')
]
