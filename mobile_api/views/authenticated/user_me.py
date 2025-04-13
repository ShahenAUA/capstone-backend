from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from mobile_api.serializers import UserGetMeSerializer
from mobile_api.utils import construct_response, construct_error, handle_validation_error
from mobile_api.messages import UNKNOWN_ERROR

class UserGetMeView(generics.ListAPIView):
    serializer_class = UserGetMeSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        security=[{'Bearer': []}],
    )
    def get(self, request):
        try:
            user = request.user
            serializer = UserGetMeSerializer(user)
            return construct_response(data=serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return handle_validation_error(e)
        except Exception as e:
            print(e)
            return construct_error(message=UNKNOWN_ERROR, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
