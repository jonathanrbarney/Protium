from rest_framework import permissions

class IsCadet(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.account_type == 'Cadet'

class IsApplicant(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.account_type == 'Applicant'

class IsInstructor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.account_type == 'Instructor'

class IsPermanentParty(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.account_type == 'Permanent Party'

class IsCoach(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.account_type == 'Coach'

class IsMedicalStaff(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.account_type == 'Medical Staff'

class IsFacilities(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.account_type == 'Facilities'

class IsAlumni(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.account_type == 'Alumni'

class IsSelf(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj
