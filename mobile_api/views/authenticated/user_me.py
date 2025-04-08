from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from mobile_api.serializers import UserGetMeSerializer
from mobile_api.utils import construct_response

class UserGetMeView(generics.ListAPIView):
    serializer_class = UserGetMeSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        security=[{'Bearer': []}],
    )
    def get(self, request):
        user = request.user
        serializer = UserGetMeSerializer(user)
        return construct_response(data=serializer.data, status=status.HTTP_200_OK)
