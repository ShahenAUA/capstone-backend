import random
import string
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from mobile_api.constants import VERIFICATION_CODE_EXPIRY_TIME, RESET_TOKEN_EXPIRY_TIME

class Profile(models.Model):
    INDIVIDUAL = "individual"
    SHELTER = "shelter"
    
    USER_TYPE_CHOICES = [
        (INDIVIDUAL, "Individual"),
        (SHELTER, "Shelter"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Enter a valid phone number.")],
        blank=True,
        null=True,
        unique=True
    )
    profile_picture = models.ImageField(upload_to="profile_pictures/", blank=True, null=True)
    verification_code = models.CharField(max_length=6, blank=True, null=True)   
    verification_code_expiry = models.DateTimeField(blank=True, null=True)
    reset_token = models.CharField(max_length=100, blank=True, null=True)
    reset_code = models.CharField(max_length=6, blank=True, null=True)
    reset_token_expiry = models.DateTimeField(blank=True, null=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default=INDIVIDUAL)

    def is_shelter(self):
        return self.user_type == self.SHELTER

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
    
    def generate_reset_token(self):
        self.reset_token = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
        self.reset_token_expiry = timezone.now() + RESET_TOKEN_EXPIRY_TIME
        self.save()
    
    def verify_reset_token(self, token):
        if not self.reset_token:
            return False
        
        if self.reset_token == token and self.reset_token_expiry > timezone.now():
            self.reset_token = None
            # self.reset_code = None
            self.reset_token_expiry = None
            self.save()
            return True
        return False
    
    def generate_reset_code(self):
        self.reset_code = ''.join(random.choices(string.digits, k=6))
        self.save()
        return self.reset_code
    
    def verify_reset_code(self, code):
        if not self.reset_code or not self.reset_token:
            return False
        if self.reset_code == code and self.reset_token_expiry > timezone.now():
            return True
        return False
     
    class Meta:
        db_table = 'profiles'
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
