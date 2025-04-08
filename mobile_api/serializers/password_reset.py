import re
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import validate_password
from django.core.validators import RegexValidator
from mobile_api.messages import (
    USER_NOT_FOUND,
    PROFILE_NOT_FOUND,
    INVALID_OR_EXPIRED_RESET_TOKEN,
    INVALID_OR_EXPIRED_RESET_CODE,
    CANNOT_RESET_TO_OLD_PASSWORD,
    USER_NOT_ACTIVE,
    INVALID_EMAIL,
    MUST_BE_6_DIGITS
)
from pet_welfare.models import Profile

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    
    def validate(self, attrs):
        email = attrs['email']
        user = None
        
        try:
            if re.match(r"[^@]+@[^@]+\.[^@]+", email):
                try:
                    user = User.objects.get(email=email)
                    profile = Profile.objects.get(user=user)
                except User.DoesNotExist:
                    raise ValidationError({'username': USER_NOT_FOUND})
            else:
                raise ValidationError({'username': INVALID_EMAIL})
            
            if not user.is_active:
                raise ValidationError({'username': USER_NOT_ACTIVE})
            
            attrs['profile'] = profile
            attrs['user'] = user
        except User.DoesNotExist:
            raise ValidationError({'username': USER_NOT_FOUND})
        except Profile.DoesNotExist:
            raise ValidationError({'username': PROFILE_NOT_FOUND})
        
        return attrs

class PasswordResetCodeVerifySerializer(serializers.Serializer):
    reset_code = serializers.CharField(required=True, write_only=True, validators=[RegexValidator(regex=r'^\d{6}$', message=MUST_BE_6_DIGITS)],)
    
    def validate(self, attrs):
        encoded_pk = self.context.get('encoded_pk')
        reset_code = attrs.get('reset_code')
        
        try:
            user_pk = force_str(urlsafe_base64_decode(encoded_pk))
            user = User.objects.get(pk=user_pk)
            profile = Profile.objects.get(user=user, reset_code=reset_code)
            
            if not user.is_active:
                raise ValidationError({'email': USER_NOT_ACTIVE})
            
            if not profile.verify_reset_code(reset_code):
                raise ValidationError({'reset_code': INVALID_OR_EXPIRED_RESET_CODE})
            
            attrs['profile'] = profile
        except User.DoesNotExist:
            raise ValidationError(USER_NOT_FOUND)
        except Profile.DoesNotExist:
            raise ValidationError(PROFILE_NOT_FOUND)
            
        
        return attrs

class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True, write_only=True, validators=[validate_password])
    
    def validate(self, attrs):
        encoded_pk = self.context.get('encoded_pk')
        token = self.context.get('token')
        
        try:
            user_pk = force_str(urlsafe_base64_decode(encoded_pk))
            user = User.objects.get(pk=user_pk)
            profile = Profile.objects.get(user=user)
            
            if not user.is_active:
                raise ValidationError({'email': USER_NOT_ACTIVE})
            
            # this check should remain the first, because verify_reset_token will clear the token if everything is correct
            if check_password(attrs.get('new_password'), user.password): 
                raise ValidationError({'new_password': CANNOT_RESET_TO_OLD_PASSWORD})
            
            if not profile.verify_reset_token(token):
                raise ValidationError({'token': INVALID_OR_EXPIRED_RESET_TOKEN})
            
            attrs['user'] = user
        except User.DoesNotExist:
            raise ValidationError({'encoded_pk': USER_NOT_FOUND})
        except Profile.DoesNotExist:
            raise ValidationError(PROFILE_NOT_FOUND)
            
        
        return attrs
