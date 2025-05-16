from rest_framework import serializers
from django.contrib.auth.models import User
from pet_welfare.models import Profile
# from pet_welfare.settings import BE_HOST_URL

class UserGetMeSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(source='profile.phone')
    user_type = serializers.CharField(source='profile.user_type')
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'date_joined', 'phone', 'user_type'] # , 'profile_picture'

    def get_full_name(self, obj):
        full_name = "%s %s" % (obj.first_name, obj.last_name)
        return full_name.strip()
    
    # def get_profile_picture(self, obj):
    #     try:
    #         profile_picture = obj.profile.profile_picture
    #         if profile_picture:
    #             return f"{BE_HOST_URL}{profile_picture.url}"
    #         return None
    #     except Profile.DoesNotExist:
    #         return None
