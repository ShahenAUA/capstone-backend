from django.urls import path, re_path

from .views import *
from .utils import schema_view

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('register_shelter', RegisterShelterView.as_view(), name='register-shelter'),
    path('verify', VerifyView.as_view(), name='verify'),
    path('login', LoginView.as_view(), name='login'),
    
    path('password-reset', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password-reset/verify-code/<str:encoded_pk>', PasswordResetCodeVerifyView.as_view(), name='password-reset-code-verify'),
    path('password-reset-confirm/<str:encoded_pk>/<str:token>', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),

    
    path('user/me', UserGetMeView.as_view(), name='user-me'),
    
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json')
]
