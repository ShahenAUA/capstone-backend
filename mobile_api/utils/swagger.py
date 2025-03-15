from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="Pet welfare app capstone API",
      default_version='v1',
      description="",
      contact=openapi.Contact(email="shahen_hovakimyan@edu.aua.am"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
