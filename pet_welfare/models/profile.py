import random
import string
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from mobile_api.constants import VERIFICATION_CODE_EXPIRY_TIME

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True, unique=True)
    profile_picture = models.ImageField(upload_to="profile_pictures/", blank=True, null=True)
    verification_code = models.CharField(max_length=6, blank=True, null=True)   
    verification_code_expiry = models.DateTimeField(blank=True, null=True)
    
    def generate_verification_code(self):
        self.verification_code = ''.join(random.choices(string.digits, k=6))
        self.verification_code_expiry = timezone.now() + VERIFICATION_CODE_EXPIRY_TIME

        self.save()
        return self.verification_code

    def verify_verification_code(self, code):
        if not self.verification_code:
            return False
        
        if self.verification_code == code and self.verification_code_expiry > timezone.now():
            self.verification_code = None
            self.verification_code_expiry = None
            self.save()
            return True
        return False
    
    class Meta:
        db_table = 'profiles'
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
