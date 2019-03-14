from rest_framework import permissions
from django.db.models import Q

class PostPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if bool(request.user and request.user.is_authenticated):
            if view.action in ['destroy']:
                if (request.user ==obj.creator):
                    return True
        return False

class VotePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if bool(request.user and request.user.is_authenticated):
            if view.action =='list':
                view.queryset=view.queryset.filter(voter=request.user)
                return True
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if bool(request.user and request.user.is_authenticated):
            if view.action in ['retrieve','partial_update', 'update', 'destroy']:
                if (request.user==obj.voter):
                    return True
                return False
        return False
