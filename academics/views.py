from django.shortcuts import render
from academics.models import *
from academics.forms import *
import django.contrib.auth as auth
import django.shortcuts as shortcuts
import django.utils.http as http
import django.views.decorators.cache as cache
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from discus.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from discus.forms import *
# Create your views here.

def departments(request):
    departments = Department.objects.all()
    form = departmentForm()
    show=False
    if request.method=='POST':
        form = departmentForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            show=True
    return shortcuts.render(request, 'academics/departments.html', {'form':form, 'departments': departments, 'show':show,})

def department(request, id):
    department = shortcuts.get_object_or_404(Department, id=id)
    eForm = courseForm(instance=department)
    cForm = courseForm()
    cShow = False
    eShow = False
    if request.method=='POST':
        if request.POST['action']=='archive':
            department.is_archived=True
            department.save()
            return shortcuts.redirect('departments')
        elif request.POST['action']=='unarchive':
            department.is_archived=False
            department.save()
            return shortcuts.redirect('departments')
        elif request.POST['action'] == 'edit':
            eForm = courseForm(request.POST, instance=department)
            if eForm.is_valid():
                eForm.save()
            else:
                eShow = True
        elif request.POST['action'] == 'create':
            cForm = courseForm(request.POST)
            if cForm.is_valid():
                course=cForm.save()
                course.creator = request.user
                course.department = department
                course.save()
            else:
                cShow = True
    return shortcuts.render(request, 'academics/department.html', {'eForm':eForm,'cForm':cForm, 'courses':department.courses.all(),
                                                           'department': department, 'cShow':cShow, 'eShow':eShow})

def course(request, id):
    course = shortcuts.get_object_or_404(Post, id=id)
    bid = course.department.id
    form = courseForm()
    show = False
    if request.method=='POST':
        if request.POST['action']=='delete':
            course.delete()
            return shortcuts.redirect(reverse('department', bid))
        elif request.POST['action'] == 'create':
            form = courseForm(request.POST)
            if form.is_valid():
                reply = form.save()
                reply.creator = request.user
                reply.reply_to = course
                reply.save()
            else:
                show = True
    return shortcuts.render(request, 'discus/course.html', {'form':form, 'replies':course.replies.all(),
                                                           'course': course, 'show':show})