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

    path('user/me', UserGetMeView.as_view(), name='user-me'),
    path('user/listings', GetListingsView.as_view(), name='get-listings'),
    path('user/listings/add', AddListingView.as_view(), name='add-listing'),
    
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json')
]
