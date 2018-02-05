from rest_framework.permissions import BasePermission
from ..enums import UserRoles


class UserPermissions(BasePermission):
    get_user_permission = UserRoles.Admin.value

    def has_object_permission(self, request, view, obj):
        # Permission logic for Get one user
        if view.action == 'retrieve':
            if obj.id == "me":
                return True
            if request.user.id != obj.id and request.user.role > self.get_user_permission:
                return False
        return True

    def has_permission(self, request, view):
        if view.action == 'login':
            return True
        if view.action == 'signup':
            return True
        if request.user.role != UserRoles.Admin.value:
            return False

        return True
