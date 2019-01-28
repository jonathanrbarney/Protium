from django.contrib.auth.models import User, Group
from rest_framework import viewsets, mixins
from academics.serializers import *
from academics.models import *
from academics.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import *
from accounts.permissions import *

class TermViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Term.objects.all()
    serializer_class = TermSerializer
    permission_classes = (IsAuthenticated,)

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (IsAuthenticated&IsOwnerOrReadOnly,)

class PeriodViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Period.objects.all()
    serializer_class = PeriodSerializer

class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class ProgramViewSet(viewsets.ModelViewSet):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer


class RequirementViewSet(viewsets.ModelViewSet):
    queryset = Course_Requirement.objects.all()
    serializer_class = RequirementSerializer
