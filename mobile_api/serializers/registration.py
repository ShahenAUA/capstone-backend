from rest_framework import serializers
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.contrib.auth.password_validation import validate_password
from pet_welfare.models import Profile
from mobile_api.utils import send_verification_email

class RegisterSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(
        required=False,
        allow_blank=True,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Enter a valid phone number.")],
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'phone']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        phone = validated_data.pop('phone', None)

        try:
            user = User.objects.create_user(
                username=validated_data['email'],
                email=validated_data['email'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                password=validated_data['password']
            )
            user.is_active = False
            user.save()

            profile = Profile.objects.create(user=user, phone=phone)
            verification_code = profile.generate_verification_code()

            send_verification_email(user.email, verification_code)

            return user

        except IntegrityError:
            raise serializers.ValidationError({"email": "A user with this email already exists."})

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
