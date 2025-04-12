import jwt
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from pet_welfare.settings import REFRESH_TOKEN_EXPIRED_STATUS_CODE, SECRET_KEY
from mobile_api.serializers import LoginSerializer, UserTokenRefreshSerializer
from mobile_api.utils import handle_validation_error, construct_error, construct_response
from mobile_api.messages import (
    UNKNOWN_ERROR,
    EXPIRED_AUTH_CREDENTIALS,
    INVALID_REFRESH_TOKEN,
    USER_NOT_FOUND,
    USER_NOT_ACTIVE
)

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
        
            return construct_response(data=serializer.validated_data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return handle_validation_error(e)
        except Exception as e:
            print(e)
            return construct_error(message=UNKNOWN_ERROR, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserTokenRefreshView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserTokenRefreshSerializer
    authentication_classes = []

    @swagger_auto_schema(
        responses={
            200: openapi.Response(description='Success', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'refresh': openapi.Schema(type=openapi.TYPE_STRING),
                    'access': openapi.Schema(type=openapi.TYPE_STRING)
                }
            ))
        },
        request_body=UserTokenRefreshSerializer
    )
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            refresh_token = serializer.validated_data.get('refresh_token')
            
            # for getting ExpiredSignatureError if token is expired
            decoded_token = jwt.decode(refresh_token, algorithms=['HS256'], key=SECRET_KEY, options={"verify_signature": True})
            
            user_id = decoded_token.get('user_id')
            
            user = User.objects.get(id=user_id)
            if not user.is_active:
                return construct_error(message=USER_NOT_ACTIVE, status=status.HTTP_400_BAD_REQUEST)
            
            refresh = RefreshToken(refresh_token)
            access_token = refresh.access_token
            
            response_data = {
                'refresh': str(refresh_token),
                'access': str(access_token)
            }

            return construct_response(data=response_data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return handle_validation_error(e)
        except User.DoesNotExist:
            return construct_error(message=USER_NOT_FOUND, status=status.HTTP_400_BAD_REQUEST)
        except jwt.ExpiredSignatureError:
            # TODO for future - delete expired refresh token from outstanding token table and its related instance from blacklisted token table if necessary (for TokenError case)
            return construct_error(message=EXPIRED_AUTH_CREDENTIALS, identifier='refresh_token', status=REFRESH_TOKEN_EXPIRED_STATUS_CODE)
        except (jwt.InvalidTokenError, TokenError) as e:
            return construct_error(message=INVALID_REFRESH_TOKEN, identifier='refresh_token', status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return construct_error(message=UNKNOWN_ERROR, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

