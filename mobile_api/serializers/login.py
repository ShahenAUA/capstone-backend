from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
# from django.core.validators import validate_email

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    # def validate_email(self, value):
    #     try:
    #         validate_email(value)
    #     except ValidationError:
    #         raise serializers.ValidationError("Invalid email address.")
        
    #     return value

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        try:
            user = User.objects.get(username=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("No user found with this email.")

        user = authenticate(username=email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid credentials.")

        if not user.is_active:
            raise serializers.ValidationError("Account is not verified.")

        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
