from django.urls import path, re_path

from .views import *
from .utils import schema_view

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('verify', VerifyView.as_view(), name='verify'),
    path('login', LoginView.as_view(), name='login'),
    
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json')
]
