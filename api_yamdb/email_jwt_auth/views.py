from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .serializers import UserEmailCodeSerializer, UserRegistrationsSerializer


class UserCreateOrSendMailCodeAPI(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationsSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserEmailCodeLoginAPI(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserEmailCodeSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
