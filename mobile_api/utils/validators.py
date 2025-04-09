import regex
from rest_framework.serializers import ValidationError
from mobile_api.constants import NameTypes
from mobile_api.messages import (INVALID_FIRST_NAME_LENGTH, INVALID_FIRST_NAME_SYMBOLS, INVALID_LAST_NAME_LENGTH, INVALID_LAST_NAME_SYMBOLS,
                                 INVALID_SHELTER_NAME_LENGTH, INVALID_SHELTER_NAME_SYMBOLS)

def validate_name(value, name_type):
    if name_type == NameTypes.FIRST_NAME:
        length_message = INVALID_FIRST_NAME_LENGTH
        symbol_message = INVALID_FIRST_NAME_SYMBOLS
    elif name_type == NameTypes.LAST_NAME:
        length_message = INVALID_LAST_NAME_LENGTH
        symbol_message = INVALID_LAST_NAME_SYMBOLS
    elif name_type == NameTypes.SHELTER_NAME:
        length_message = INVALID_SHELTER_NAME_LENGTH
        symbol_message = INVALID_SHELTER_NAME_SYMBOLS
    
    max_length = 50
    if len(value) > max_length:
        raise ValidationError(length_message)
    if not regex.match(r'^\p{L}[\p{L}\p{M}\s-]{1,}$', value):
        raise ValidationError(symbol_message)
    
    return value