from django.urls import path
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import (UserCreateAPIView, UserListAPIView, UserRetrieveAPIView, UserUpdateAPIView, UserDestroyAPIView,
                         ResetPassword, ResetPasswordConfirm)

app_name = UsersConfig.name

urlpatterns = [
    path('register/', UserCreateAPIView.as_view(permission_classes=(AllowAny,)), name='users_register'),
    path('list/', UserListAPIView.as_view(), name='users_list'),
    path('retrieve/<int:pk>/', UserRetrieveAPIView.as_view(), name='users_retrieve'),
    path('update/<int:pk>/', UserUpdateAPIView.as_view(), name='users_update'),
    path('delete/<int:pk>/', UserDestroyAPIView.as_view(), name='users_delete'),
    path('login/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),
    path('reset_password/', ResetPassword.as_view(), name='reset_password'),
    path('reset_password_confirm/', ResetPasswordConfirm.as_view(), name='reset_password_confirm'),
]
