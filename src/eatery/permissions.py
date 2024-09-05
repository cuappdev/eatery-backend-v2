from rest_framework import permissions


class EateryPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action in ["list", "retrieve"]:
            return True
        return request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if view.action in ["retrieve"]:
            return True
        return request.user.is_staff
