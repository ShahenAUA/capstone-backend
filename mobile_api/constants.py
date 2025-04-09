from datetime import timedelta
from enum import StrEnum

VERIFICATION_CODE_EXPIRY_TIME = timedelta(minutes=10)
RESET_TOKEN_EXPIRY_TIME = timedelta(minutes=10)

class NameTypes(StrEnum):
    FIRST_NAME = "FIRST_NAME",
    LAST_NAME = "LAST_NAME",
    SHELTER_NAME = "SHELTER_NAME"
