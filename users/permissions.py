from rest_framework.permissions import BasePermission


class IsAuthor(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == obj.author


class IsAdministrator(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.groups.filter(name='Администраторы').exists()
