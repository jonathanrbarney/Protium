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
    form = departmentEdit()
    show=False
    if request.method=='POST':
        form = departmentEdit(request.POST)
        if form.is_valid():
            form.save()
        else:
            show=True
    return shortcuts.render(request, 'academics/departments.html', {'form':form, 'departments': departments, 'show':show,})

def department(request, id):
    department = shortcuts.get_object_or_404(Department, id=id)
    eForm = departmentEdit(instance=department)
    cForm = postForm()
    cShow = False
    eShow = False
    if request.method=='POST':
        if request.POST['action']=='archive':
            department.is_archived=True
            department.save()
            return shortcuts.redirect('boards')
        elif request.POST['action']=='unarchive':
            department.is_archived=False
            department.save()
            return shortcuts.redirect('boards')
        elif request.POST['action'] == 'edit':
            eForm = boardForm(request.POST, instance=board)
            if eForm.is_valid():
                eForm.save()
            else:
                eShow = True
        elif request.POST['action'] == 'create':
            cForm = postForm(request.POST)
            if cForm.is_valid():
                post=cForm.save()
                post.creator = request.user
                post.board = board
                post.save()
            else:
                cShow = True
    return shortcuts.render(request, 'discus/board.html', {'eForm':eForm,'cForm':cForm, 'posts':board.posts.all(),
                                                           'board': board, 'cShow':cShow, 'eShow':eShow})

def post(request, id):
    post = shortcuts.get_object_or_404(Post, id=id)
    bid = post.board.id
    form = postForm()
    show = False
    if request.method=='POST':
        if request.POST['action']=='delete':
            post.delete()
            return shortcuts.redirect(reverse('board', bid))
        elif request.POST['action'] == 'create':
            form = postForm(request.POST)
            if form.is_valid():
                reply = form.save()
                reply.creator = request.user
                reply.reply_to = post
                reply.save()
            else:
                show = True
    return shortcuts.render(request, 'discus/post.html', {'form':form, 'replies':post.replies.all(),
                                                           'post': post, 'show':show})