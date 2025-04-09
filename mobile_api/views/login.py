from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ValidationError
from rest_framework import status
from mobile_api.serializers import LoginSerializer
from mobile_api.utils import handle_validation_error, construct_error, construct_response
from mobile_api.messages import UNKNOWN_ERROR

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
        
            return construct_response(data=serializer.validated_data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return handle_validation_error(e)
        except Exception as e:
            print(e)
            return construct_error(message=UNKNOWN_ERROR, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
