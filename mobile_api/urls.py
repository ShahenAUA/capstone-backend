from django.urls import include, path, re_path
from rest_framework import routers

from .views import *
from .utils import schema_view

urlpatterns = [
    
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json')
]
