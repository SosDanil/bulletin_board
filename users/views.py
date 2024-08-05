from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from users.models import User
from users.permissions import IsUserHimself
from users.serializers import UserSerializer, UserCreateUpdateSerializer


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateUpdateSerializer

    def perform_create(self, serializer):
        obj = serializer.save(is_active=True)
        obj.set_password(self.request.data['password'])
        obj.save()


class UserListAPIView(ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)


class UserRetrieveAPIView(RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsUserHimself,)


class UserUpdateAPIView(UpdateAPIView):
    serializer_class = UserCreateUpdateSerializer
    queryset = User.objects.all()
    permission_classes = (IsUserHimself,)


class UserDestroyAPIView(DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = (IsUserHimself,)
