from rest_framework import permissions
from accounts.serializers import *

class AccountPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if bool(request.user and request.user.is_authenticated):
                return True
        return False

    def has_object_permission(self, request, view, obj):
        if bool(request.user and request.user.is_authenticated):
            if view.action in ['partial_update', 'update']:
                if (request.user == obj):
                    return True
            if view.action == 'retrieve':
                if (request.user == obj):
                    view.serializer=OwnAccountSerializer
                else:
                    view.serializer=PublicAccountSerializer
            if view.action =='create':
                view.serializer=CreateAccountSerializer
                return True
        return False

class CreationTicketPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if bool(request.user and request.user.is_authenticated):
                if view.action =='list':
                    view.queryset=view.queryset.filter(issuer=request.user)
                return True
        return False

    def has_object_permission(self, request, view, obj):
        if bool(request.user and request.user.is_authenticated):
            if view.action in ['retrieve','destroy']:
                if request.user ==obj.issuer:
                    return True
                return False
        return False

