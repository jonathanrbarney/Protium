from rest_framework import permissions
from django.db.models import Q
from military.models import *

class PositionPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if bool(request.user and request.user.is_authenticated):
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if bool(request.user and request.user.is_authenticated):
            if view.action in ['partial_update', 'update', 'destroy']:
                if len({*request.user.jobs.all()} & {*get_all_supervisors(obj)}) > 0:
                    return True
                return False
            return True
        return False

class MilScorePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if bool(request.user and request.user.is_authenticated):
            if view.action =='list':
                subs=get_all_account_subordinates(request.user)
                sub_holders=[]
                for i in subs:
                    sub_holders.append(i.holder)
                view.queryset=view.queryset.filter(Q(cadet=request.user)
                                                |Q(cadet__in=subs))
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if bool(request.user and request.user.is_authenticated):
            if view.action in ['retrieve','partial_update', 'update', 'destroy']:
                if len({*request.user.jobs.all()} & {*get_all_account_supervisors(obj.cadet)}) > 0:
                    return True
                return False
            return True
        return False

class UnitPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if bool(request.user and request.user.is_authenticated):
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if bool(request.user and request.user.is_authenticated):
            if view.action in ['partial_update', 'update', 'destroy']:
                valid=list(obj.commanders.all())
                for i in obj.commanders.all():
                    valid=valid+get_all_supervisors(i)
                if len({*request.user.jobs.all()} & {*valid}) > 0:
                    return True
                return False
            return True
        return False