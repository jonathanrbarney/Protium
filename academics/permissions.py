from rest_framework import permissions
from django.db.models import Q

class CoursePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if bool(request.user and request.user.is_authenticated):
            if view.action == 'list':
                view.queryset = view.queryset.filter((Q(admins__in=[request.user])|
                                                     Q(instructors__in=[request.user])|
                                                     Q(public=True))&
                                                     Q(is_archived=False)).distinct()
                return True
            else:
                return True
        return False

    def has_object_permission(self, request, view, obj):
        if bool(request.user and request.user.is_authenticated):
            if view.action =='retrieve':
                return True
            elif view.action in ['partial_update', 'update', 'destroy']:
                if (request.user in obj.admins.all()) or (request.user in obj.department.admins.all()):
                    return True
        return False

class SectionPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if bool(request.user and request.user.is_authenticated):
            if view.action == 'list':
                return True
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if bool(request.user and request.user.is_authenticated):
            if view.action =='retrieve':
                return True
            elif view.action in ['partial_update', 'update', 'destroy']:
                if (request.user in obj.course.admins.all()) or (request.user in obj.department.admins.all()):
                    return True
        return False

class EnrollmentPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if bool(request.user and request.user.is_authenticated):
            if view.action == 'list':
                view.queryset = view.queryset.filter(Q(registration__student=request.user)
                                                     |Q(registration__student__academic_advisor=request.user)
                                                     |Q(section__instructors__in=[request.user])
                                                     |Q(section__course__department__admins__in=[request.user])).distinct()
                return True
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if bool(request.user and request.user.is_authenticated):
            if view.action  in ['partial_update', 'update', 'destroy','retrieve']:
                if ((request.user == obj.registration.student)
                    or( request.user == obj.registration.student.academic_advisor)
                    or(request.user in obj.section.instructors.all())
                    or(request.user in obj.section.course.instructors.all())
                    or(request.user in obj.section.course.department.admins.all())):
                    return True
                return False
        return False

class RegistrationPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if bool(request.user and request.user.is_authenticated):
            if view.action == 'list':
                view.queryset = view.queryset.filter(Q(student=request.user)
                                                     |Q(student__academic_advisor=request.user)
                                                     |Q(course__instructors__in=[request.user])
                                                     |Q(course__admins__in=[request.user])
                                                     |Q(course__department__admins__in=[request.user])).distinct()
                return True
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if bool(request.user and request.user.is_authenticated):
            if view.action  in ['partial_update', 'update', 'destroy','retrieve']:
                if ((request.user == obj.student)
                    or( request.user == obj.student.academic_advisor)
                    or(request.user in obj.course.instructors.all())
                    or(request.user in obj.course.admins.all())
                    or(request.user in obj.course.department.admins.all())):
                    return True
                return False
        return False

class CompletionPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if bool(request.user and request.user.is_authenticated):
            if view.action == 'list':
                view.queryset = view.queryset.filter(Q(student=request.user)
                                                     |Q(student__academic_advisor=request.user)
                                                     |Q(course__department__admins__in=[request.user])).distinct()
                return True
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if bool(request.user and request.user.is_authenticated):
            if view.action =='retrieve':
                if ((request.user == obj.student)
                    or( request.user == obj.student.academic_advisor)
                    or(request.user in obj.course.instructors.all())
                    or(request.user in obj.course.admins.all())
                    or(request.user in obj.course.department.admins.all())):
                    return True
            if view.action  in ['partial_update', 'update', 'destroy']:
                if ((request.user in obj.course.instructors.all())
                    or(request.user in obj.course.admins.all())
                    or(request.user in obj.course.department.admins.all())):
                    return True
                return False
        return False

class DepartmentPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if bool(request.user and request.user.is_authenticated):
            if view.action  in ['partial_update', 'update',]:
                if (request.user in obj.course.admins.all()):
                    return True
                return False
        return False

class ProgramPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if bool(request.user and request.user.is_authenticated):
            if view.action  in ['partial_update', 'update', 'destroy']:
                if request.user in obj.department.admins.all():
                    return True
                return False
        return False

class RequirementPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if bool(request.user and request.user.is_authenticated):
            if view.action  in ['partial_update', 'update', 'destroy']:
                if request.user in obj.program.department.admins.all():
                    return True
                return False
        return False