from rest_framework import permissions

class IsTutor(permissions.BasePermission):
    """Define permissions for a tutor"""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_tutor
    
class IsAuthenticatedOrTokenRefresh(permissions.BasePermission):
    """
    Custom permission to check if the user is authenticated or accessing the token refresh endpoint.
    """
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return True
        return request.path == '/account/token/refresh/'
