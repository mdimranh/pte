from rest_framework.permissions import BasePermission


class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin

class IsStudentPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_student

class IsStudentPermissionOrReadonly(BasePermission):
    def has_permission(self, request, view):
        return (not request.user.is_authenticated or request.user.is_student)


class IsOrganizationPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_organization
