from typing import Optional
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.auth.hashers import check_password
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ValidationError
from operator import itemgetter
from mobile_api.serializers import PasswordResetRequestSerializer, PasswordResetCodeVerifySerializer, PasswordResetConfirmSerializer
from pet_welfare.models import Profile
from pet_welfare import settings
from mobile_api.messages import (
    RESET_CODE_SENT,
    RESET_CODE_VERIFIED,
    PASSWORD_RESET_SUCCESSFULLY,
    CANNOT_RESET_TO_OLD_PASSWORD
)
from mobile_api.utils import construct_response, construct_error, handle_validation_error # , bulk_logout

class PasswordResetRequestView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PasswordResetRequestSerializer
    authentication_classes = []

    @swagger_auto_schema(
        operation_description="Send reset code to user's email",
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Reset code/link sent",
                examples={
                    "application/json": {
                        "message": RESET_CODE_SENT,
                        "identifier": "encoded_pk"
                    },
                }
            )
        },
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
    )
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data.get('user')
            profile: Optional[Profile] = serializer.validated_data.get('profile')
            
            profile.generate_reset_token()
            
            encoded_pk = urlsafe_base64_encode(force_bytes(user.pk))
            
            reset_code = profile.generate_reset_code()
            
            subject = 'Password Reset Request'
            message = render_to_string('password_reset_email_with_code.html', {'reset_code': reset_code})
            recipients = [user.email]
            send_mail(subject, message, settings.FROM_EMAIL, recipients, fail_silently=False)
            
            return construct_response(message=RESET_CODE_SENT, data={'identifier': encoded_pk}, status=status.HTTP_200_OK)
        except ValidationError as e:
            return handle_validation_error(e)

class PasswordResetCodeVerifyView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PasswordResetCodeVerifySerializer
    authentication_classes = []

    def post(self, request, encoded_pk):
        try:
            serializer = self.serializer_class(data=request.data, context={'encoded_pk': encoded_pk})
            serializer.is_valid(raise_exception=True)
            
            profile: Optional[Profile] = serializer.validated_data.get('profile')
            
            data = {
                'identifier': encoded_pk,
                'reset_token': profile.reset_token,
            }
            
            return construct_response(message=RESET_CODE_VERIFIED, data=data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return handle_validation_error(e)

class PasswordResetConfirmView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PasswordResetConfirmSerializer
    authentication_classes = []

    def post(self, request, encoded_pk, token):
        try:
            serializer = self.get_serializer(data=request.data, context={'encoded_pk': encoded_pk, 'token': token})
            serializer.is_valid(raise_exception=True)
            user, new_password = itemgetter('user', 'new_password')(serializer.validated_data)
            
            if check_password(new_password, user.password):
                return construct_error(message=CANNOT_RESET_TO_OLD_PASSWORD, identifier='new_password', status=status.HTTP_400_BAD_REQUEST)
            
            user.set_password(new_password)
            user.save()
            
            # bulk_logout(user=user)
            
            return construct_response(message=PASSWORD_RESET_SUCCESSFULLY, status=status.HTTP_200_OK)
        except ValidationError as e:
            return handle_validation_error(e)
