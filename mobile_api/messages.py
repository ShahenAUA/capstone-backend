from django.utils.translation import gettext_lazy as _

# success
VERIFIED_SUCCESS = _('Account verified successfully')
RESET_CODE_SENT = _('Password reset code has been sent to your email.')
RESET_CODE_VERIFIED = _('Password reset code has been verified.')
PASSWORD_RESET_SUCCESSFULLY = _('Password has been reset successfully.')

# errors
VALIDATION_ERROR = _('Validation error occurred.')
UNKNOWN_ERROR = _('Unknown error occured')
INVALID_FIRST_NAME_LENGTH = _('First name exceeds the maximum length.')
INVALID_LAST_NAME_LENGTH = _('Last name exceeds the maximum length.')
INVALID_FIRST_NAME_SYMBOLS = _('First name can only contain letters, spaces, and hyphens (at least 2 symbols).')
INVALID_LAST_NAME_SYMBOLS = _('Last name can only contain letters, spaces, and hyphens (at least 2 symbols).')
INVALID_SHELTER_NAME_LENGTH = _('Shelter name exceeds the maximum length.')
INVALID_SHELTER_NAME_SYMBOLS = _('Shelter name can only contain letters, spaces, and hyphens (at least 2 symbols).')
USER_EXISTS = _('A user with this email already exists.')
INVALID_PHONE = _('Enter a valid phone number.')
PHONE_EXISTS = _('A user with this phone already exists.')
SHELTER_EXISTS = _('A shelter with this registration number already exists.')

CANNOT_RESET_TO_OLD_PASSWORD = _('You are trying to use your old password as your new one.')
USER_NOT_FOUND = _('User not found.')
PROFILE_NOT_FOUND = _('Profile not found.')
INVALID_OR_EXPIRED_RESET_TOKEN = _('Invalid or expired reset token.')
INVALID_OR_EXPIRED_RESET_CODE = _('Invalid or expired reset code.')
USER_NOT_ACTIVE = _('User is not active. Make sure you confirmed your email.')
INVALID_EMAIL = _('You should enter your email correctly.')
MUST_BE_6_DIGITS = _('This field must be exactly 6 digits.')
