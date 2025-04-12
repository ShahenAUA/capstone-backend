from django.contrib.auth.models import User
from rest_framework import status, generics
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ValidationError
from pet_welfare.models import Profile, ShelterProfile
from mobile_api.serializers import RegisterSerializer, RegisterShelterSerializer, VerifySerializer
from mobile_api.utils import send_verification_email, handle_validation_error, construct_error, construct_response
from mobile_api.messages import REGISTERED_SUCCESS, VERIFIED_SUCCESS, UNKNOWN_ERROR

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data.get('phone', None)
        email = serializer.validated_data.get('email', None)
        first_name = serializer.validated_data.get('first_name', None)
        last_name = serializer.validated_data.get('last_name', None)
        password = serializer.validated_data.get('password', None)

        try:
            user = User.objects.create_user(
                username=email,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password
            )
            user.is_active = False
            user.save()

            profile = Profile.objects.create(user=user, phone=phone)
            verification_code = profile.generate_verification_code()

            send_verification_email(user.email, verification_code)

            return construct_response(message=REGISTERED_SUCCESS, data={"user_id": user.id}, status=status.HTTP_200_OK)
        except ValidationError as e:
            return handle_validation_error(e)
        except Exception as e:
            print(e)
            return construct_error(message=UNKNOWN_ERROR, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class RegisterShelterView(generics.CreateAPIView):
    serializer_class = RegisterShelterSerializer
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            phone = serializer.validated_data.get('phone', None)
            registration_number = serializer.validated_data.get('registration_number', None)
            name = serializer.validated_data.get('name', None)
            email = serializer.validated_data.get('email', None)
            password = serializer.validated_data.get('password', None)

            user = User.objects.create_user(
                username=email,
                email=email,
                first_name=name,
                # last_name='', # TODO - review this
                password=password
            )
            user.is_active = False
            user.save()

            profile = Profile.objects.create(user=user, phone=phone)
            ShelterProfile.objects.create(profile=profile, registration_number=registration_number, name=name)
            verification_code = profile.generate_verification_code()

            send_verification_email(user.email, verification_code)

            return construct_response(message=REGISTERED_SUCCESS, data={"user_id": user.id}, status=status.HTTP_200_OK)
        except ValidationError as e:
            return handle_validation_error(e)
        except Exception as e:
            print(e)
            return construct_error(message=UNKNOWN_ERROR, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
class VerifyView(generics.GenericAPIView):
    serializer_class = VerifySerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            return construct_response(message=VERIFIED_SUCCESS, status=status.HTTP_200_OK)
        except ValidationError as e:
            return handle_validation_error(e)
        except Exception as e:
            print(e)
            return construct_error(message=UNKNOWN_ERROR, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    