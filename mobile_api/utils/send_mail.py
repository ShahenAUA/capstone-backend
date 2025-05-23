from django.core.mail import send_mail
from pet_welfare import settings

def send_verification_email(email, code):
    subject = "Verify Your Account"
    message = f"Your verification code is {code}"
    send_mail(subject, message, settings.FROM_EMAIL, [email])
