from rest_framework import permissions

class ReportPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action in ['create']:
            return True
        return request.user.is_staff
                                                                                                
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff