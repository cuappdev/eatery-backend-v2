from rest_framework import permissions

class ReportPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action in ['create', 'custom_retrieve']:
            return True
        return request.user.is_staff
                                                                                                
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff