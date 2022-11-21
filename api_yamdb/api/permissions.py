from rest_framework import permissions

UPDATE_ERROR_TEXT = 'Изменение чужого контента запрещено!'


class IsAuthorOrStaffOrReadOnly(permissions.BasePermission):
    message = UPDATE_ERROR_TEXT

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated
                and (request.user.is_admin or request.user.is_moderator))
            or obj.author == request.user
        )


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user and request.user.is_authenticated
                and request.user.is_admin)


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
