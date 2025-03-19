from rest_framework import serializers
from django.contrib.auth.models import User
from pet_welfare.models import Profile
# from pet_welfare.settings import BE_HOST_URL

class UserGetMeSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(source='profile.phone')
    # type = serializers.CharField(source='profile.type')
    # profile_picture = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'date_joined', 'phone'] # 'type', 'profile_picture'

    # def get_profile_picture(self, obj):
    #     try:
    #         profile_picture = obj.profile.profile_picture
    #         if profile_picture:
    #             return f"{BE_HOST_URL}{profile_picture.url}"
    #         return None
    #     except Profile.DoesNotExist:
    #         return None
