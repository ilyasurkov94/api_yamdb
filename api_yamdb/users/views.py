from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from .permissions import IsAdminPermission, IsOwnerPermission
from .models import User
from .serializers import UserSerializer


class UserAdminViewset(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminPermission,)

    @action(detail=False, methods=['get', 'patch'], permission_classes=[IsOwnerPermission])
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = self.serializer_class(user)
            return Response(serializer.data)
        elif request.method == 'PATCH':
            serializer = self.serializer_class(
                request.user,
                data=request.data,
                partial=True,
                context={'request': request}
            )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
