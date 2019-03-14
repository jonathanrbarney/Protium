from django.contrib.auth.models import User, Group
from rest_framework import viewsets, mixins
from academics.serializers import *
from academics.models import *
from rest_framework.permissions import *
from academics.permissions import *
from rest_framework.filters import SearchFilter, OrderingFilter


class TermViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Term.objects.all()
    serializer_class = TermSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['id', 'from_date', 'name', 'to_date']
    ordering_fields = ['id', 'from_date', 'name', 'to_date']


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated & CoursePermission]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'abbreviation', 'summary', 'academic_credit_hours', 'military_credit_hours',
                     'athletic_credit_hours']
    search_fields = ['name', 'abbreviation', 'summary', 'academic_credit_hours', 'military_credit_hours',
                     'athletic_credit_hours']
    ordering = ['name']


class PeriodViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Period.objects.all()
    serializer_class = PeriodSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['id', 'name']
    ordering_fields = ['id', 'name']
    ordering = ['name']


class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [IsAuthenticated & SectionPermission]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['id', 'from_date', 'name', 'to_date']
    ordering_fields = ['id', 'from_date', 'name', 'to_date']


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated & EnrollmentPermission]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['section__term__name']
    ordering_fields = ['section__term__from_date', 'section__term__to_date']


class RegistrationViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin,
                          mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [IsAuthenticated & RegistrationPermission]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['id', 'student__id', 'course__id', 'section__term']
    ordering_fields = ['number__grade', 'student__id', 'section__term']


class CompletionViewSet(viewsets.ModelViewSet):
    queryset = Completion.objects.all()
    serializer_class = CompletionSerializer
    permission_classes = [IsAuthenticated & CompletionPermission]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['id', 'student__id', 'course__id']
    ordering_fields = ['number_grade', 'letter_grade', 'course__name']
    ordering = ['course__name']


class DepartmentViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin,
                        viewsets.GenericViewSet):
    queryset = Department.objects.all().filter(is_archived=False)
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated & DepartmentPermission]
    search_fields = ['id', 'name', 'abbreviation', 'admins__id', 'instructors__id', 'summary']
    ordering_fields = ['name', 'abbreviation']
    ordering = ['name']


class ProgramViewSet(viewsets.ModelViewSet):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer


class RequirementViewSet(viewsets.ModelViewSet):
    queryset = Course_Requirement.objects.all()
    serializer_class = RequirementSerializer
