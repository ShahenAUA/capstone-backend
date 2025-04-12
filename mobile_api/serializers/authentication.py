from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from mobile_api.messages import ACTIVATE_BEFORE_LOGIN, UNABLE_TO_LOGIN

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        try:
            user = User.objects.get(username=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(UNABLE_TO_LOGIN)

        if not user.is_active:
            raise serializers.ValidationError(ACTIVATE_BEFORE_LOGIN)
        
        user = authenticate(username=email, password=password)
        if not user:
            raise serializers.ValidationError(UNABLE_TO_LOGIN)

        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

class UserTokenRefreshSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True)
