import json
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ImproperlyConfigured
from pathlib import Path
from pet_welfare import settings
from mobile_api.serializers import GetSpeciesByTypeSerializer
from mobile_api.utils import construct_error, construct_response, handle_validation_error
from rest_framework import status

class GetSpeciesView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = GetSpeciesByTypeSerializer
    authentication_classes = []
    
    def get_species_data(self):
        try:
            species_json_path = Path(settings.BASE_DIR) / 'species.json'

            if not species_json_path.exists():
                raise ImproperlyConfigured(f"species.json not found at {species_json_path}")

            with open(species_json_path, 'r', encoding='utf-8-sig') as file:
                return json.load(file)
        
        except FileNotFoundError:
            raise ImproperlyConfigured("species.json file not found.")
        except json.JSONDecodeError:
            raise ImproperlyConfigured("Error decoding species.json file.")
        except UnicodeDecodeError:
            raise ImproperlyConfigured("Error decoding species.json file due to encoding issues.")
        
    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description='Success',
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_STRING)
                )
            ),
            400: openapi.Response(description='Invalid Input'),
            404: openapi.Response(description='Species Not Found'),
            500: openapi.Response(description='Server Error'),
        },
        query_serializer=GetSpeciesByTypeSerializer
    )
    def get(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.query_params)
            serializer.is_valid(raise_exception=True)

            species_type = serializer.validated_data['type']
            
            species_data = self.get_species_data()

            if species_type not in species_data:
                return construct_error(message="Species not found", status=status.HTTP_404_NOT_FOUND)

            return construct_response(data=species_data[species_type], status=status.HTTP_200_OK)

        except ValidationError as e:
            return handle_validation_error(e)

        except ImproperlyConfigured as e:
            return construct_error(message=str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            print(e)
            return construct_error(message="An unexpected error occurred", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
