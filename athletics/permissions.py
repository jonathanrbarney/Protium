from rest_framework import permissions

class AthScore(permissions.BasePermission):
    def has_permission(self, request, view):
        if bool(request.user and request.user.is_authenticated):
            if view.action == 'list':
                if (request.user.account_type == 'Coach'):
                    return True
                else:
                    view.queryset = view.queryset.filter(cadet=request.user)
                    return True
            elif view.action == 'create':
                if request.user.account_type == 'Coach':
                    return True
            elif view.action in ['partial_update', 'update', 'destroy']:
                if request.user.account_type == 'Coach':
                    return True
            elif view.action == 'retrieve':
                    return True
        return False

    def has_object_permission(self, request, view, obj):
        if bool(request.user and request.user.is_authenticated):
            if view.action == 'retrieve':
                if (request.user == obj.cadet) | (request.user.account_type == 'Coach'):
                    return True
        return False

