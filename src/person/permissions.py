from rest_framework import permissions

class StudentPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return False
                                                                                                
    def has_object_permission(self, request, view, obj):
        return False
    
class ChefPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return False
                                                                                                
    def has_object_permission(self, request, view, obj):
        return False