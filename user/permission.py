from rest_framework.permissions import BasePermission


class IsSuperuserOrGetPutSelfOnly(BasePermission):
    def has_permission(self, request, view):
        if view.kwargs.get('pk') is not None:
            return int(view.kwargs['pk']) == request.user.id
        return request.user.is_superuser
