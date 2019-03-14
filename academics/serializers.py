from rest_framework import serializers
from academics.models import *

class TermSerializer(serializers.ModelSerializer):
    class Meta:
        model = Term
        fields = '__all__'
        read_only_fields = ('is_active',)

from rest_framework.exceptions import PermissionDenied

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ('id','is_active','creator',)

    def validate(self, data):
        request = self.context.get("request")
        if request and request.user and data['department']:
            if request.user not in data["department"].admins.all():
                raise PermissionDenied
        return super(CourseSerializer, self).validate(data)

    def save(self, **kwargs):
        if (self.instance is None) or (self.instance and (self.instance.creator is None)):
            request = self.context.get("request")
            self.validated_data['creator']=request.user
        return super(CourseSerializer, self).save(**kwargs)


class PeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Period
        fields = '__all__'

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = '__all__'
        read_only_fields = ('id','is_active', 'creator',)

    def validate(self, data):
        request = self.context.get("request")
        if request and request.user and data['course']:
            if (request.user not in data["course"].admins.all()) and (request.user not in data["course"].department.admins.all()):
                raise PermissionDenied
        return super(SectionSerializer, self).validate(data)

    def save(self, **kwargs):
        if (self.instance is None) or (self.instance and (self.instance.creator is None)):
            request = self.context.get("request")
            self.validated_data['creator'] = request.user
        return super(SectionSerializer, self).save(**kwargs)


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'
        read_only_fields = ('id', 'creator',)

    def validate(self, data):
        request = self.context.get("request")
        if bool(request.user and request.user.is_authenticated):
            if ((request.user == data['registration'].student)
                or( request.user == data['registration'].student.academic_advisor)
                or(request.user in data['section'].instructors.all())
                or(request.user in data['section'].course.instructors.all())
                or(request.user in data['section'].course.department.admins.all())):
                pass
            else:
                raise PermissionDenied
        else:
            raise PermissionDenied
        return super(EnrollmentSerializer, self).validate(data)

    def save(self, **kwargs):
        if (self.instance is None) or (self.instance and (self.instance.creator is None)):
            request = self.context.get("request")
            self.validated_data['creator'] = request.user
        return super(EnrollmentSerializer, self).save(**kwargs)

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = '__all__'
        read_only_fields = ('id', 'creator', 'number_grade',)

    def validate(self, data):
        request = self.context.get("request")
        if bool(request.user and request.user.is_authenticated):
            if ((request.user == data['student'])
                or( request.user == data['student'].academic_advisor)
                or(request.user in data['course'].instructors.all())
                or(request.user in data['course'].admins.all())
                or(request.user in data['course'].department.admins.all())):
                pass
            else:
                raise PermissionDenied
        else:
            raise PermissionDenied
        return super(RegistrationSerializer, self).validate(data)

    def save(self, **kwargs):
        if (self.instance is None) or (self.instance and (self.instance.creator is None)):
            request = self.context.get("request")
            self.validated_data['creator'] = request.user
        return super(RegistrationSerializer, self).save(**kwargs)

class CompletionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = '__all__'
        read_only_fields = ('id', 'creator', 'number_grade',)

    def validate(self, data):
        request = self.context.get("request")
        if bool(request.user and request.user.is_authenticated):
            if ((request.user in data['course'].instructors.all())
                or(request.user in data['course'].admins.all())
                or(request.user in data['course'].department.admins.all())):
                pass
            else:
                raise PermissionDenied
        else:
            raise PermissionDenied
        return super(CompletionSerializer, self).validate(data)

    def save(self, **kwargs):
        if (self.instance is None) or (self.instance and (self.instance.creator is None)):
            request = self.context.get("request")
            self.validated_data['creator'] = request.user
        return super(CompletionSerializer, self).save(**kwargs)


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'
        read_only_fields = ('id',)


class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = '__all__'
        read_only_fields = ('id',)

    def validate(self, data):
        request = self.context.get("request")
        if bool(request.user and request.user.is_authenticated):
            if (request.user in data['department'].admins.all()):
                pass
            else:
                raise PermissionDenied
        else:
            raise PermissionDenied
        return super(ProgramSerializer, self).validate(data)


class RequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course_Requirement
        fields = '__all__'
        read_only_fields = ('id',)

    def validate(self, data):
        request = self.context.get("request")
        if bool(request.user and request.user.is_authenticated):
            if (request.user in data['program'].department.admins.all()):
                pass
            else:
                raise PermissionDenied
        else:
            raise PermissionDenied
        return super(RequirementSerializer, self).validate(data)
