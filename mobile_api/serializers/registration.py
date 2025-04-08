from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, validate_email
from django.contrib.auth.password_validation import validate_password
from pet_welfare.models import Profile, ShelterProfile
from mobile_api.utils import send_verification_email, validate_name
from mobile_api.constants import NameTypes
from mobile_api.messages import USER_EXISTS, INVALID_PHONE, PHONE_EXISTS, SHELTER_EXISTS

class RegisterSerializer(serializers.Serializer):
    email = serializers.CharField(required=True, validators=[validate_email])
    first_name = serializers.CharField(required=True, validators=[lambda value: validate_name(value, name_type=NameTypes.FIRST_NAME)])
    last_name = serializers.CharField(required=True, validators=[lambda value: validate_name(value, name_type=NameTypes.LAST_NAME)])
    phone = serializers.CharField(
        required=False,
        allow_blank=True,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message=INVALID_PHONE)],
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(USER_EXISTS)
        return value
    
    def validate_phone(self, value):
        if Profile.objects.filter(phone=value).exists():
            raise serializers.ValidationError(PHONE_EXISTS)
        return value

class RegisterShelterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    name = serializers.CharField(required=True, validators=[lambda value: validate_name(value, name_type=NameTypes.SHELTER_NAME)])
    registration_number = serializers.CharField(max_length=50)
    phone = serializers.CharField(
        required=False,
        allow_blank=True,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message=INVALID_PHONE)],
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(USER_EXISTS)
        return value
    
    def validate_phone(self, value):
        if Profile.objects.filter(phone=value).exists():
            raise serializers.ValidationError(PHONE_EXISTS)
        return value
    
    def validate_registration_number(self, value):
        if ShelterProfile.objects.filter(registration_number=value).exists():
            raise serializers.ValidationError(SHELTER_EXISTS)
        return value

class VerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        email = data.get('email')
        code = data.get('code')

        try:
            user = User.objects.get(username=email)
            profile = Profile.objects.get(user=user)
        except (User.DoesNotExist, Profile.DoesNotExist):
            raise serializers.ValidationError("Invalid email or code.")

        if not profile.verify_verification_code(code):
            raise serializers.ValidationError("Invalid verification code.")

        user.is_active = True
        user.save()

        return data
