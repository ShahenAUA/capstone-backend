from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

def bulk_logout(user):
    tokens = OutstandingToken.objects.filter(user=user)
    for token in tokens:
        try:
            token_obj = RefreshToken(token.token)
            token_obj.check_blacklist()
            token_obj.blacklist()
        except TokenError as e:
            pass
        except Exception as e:
            print(e)
        # TODO - consider tokens.delete()
        