import secrets

from django.core.mail import send_mail
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from config.settings import EMAIL_HOST_USER
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
    permission_classes = (IsUserHimself, IsAuthenticated)


class UserUpdateAPIView(UpdateAPIView):
    serializer_class = UserCreateUpdateSerializer
    queryset = User.objects.all()
    permission_classes = (IsUserHimself, IsAuthenticated)


class UserDestroyAPIView(DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = (IsUserHimself, IsAuthenticated)


class ResetPassword(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request):
        email = request.data['email']
        token = secrets.token_hex(8)
        user = request.user
        user.token = token
        user.save()

        uid = request.user.pk
        host = request.get_host()
        url = f"http://{host}/uid:{uid}/token:{token}/"
        send_mail(
            subject='Восстановление пароля',
            message=f'Привет! Держите ссылку: {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[email],
        )
        return Response({"message": "Письмо отправлено на почту"})


class ResetPasswordConfirm(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request):
        uid = request.data['uid']
        token = request.data['token']
        new_password = request.data['new_password']

        if uid == request.user.pk and token == request.user.token:
            user = request.user
            user.set_password(new_password)
            user.save()

            return Response({"message": "Пароль успешно сменен"})
