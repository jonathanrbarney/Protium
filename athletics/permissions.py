from rest_framework import permissions


class IsCoach(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.account_type == 'Coach'

class IsSelf(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.cadet
