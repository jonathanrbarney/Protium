import django.contrib.auth as auth
import django.shortcuts as shortcuts
import accounts.forms as forms
import django.utils.http as http
import django.views.decorators.cache as cache
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from accounts.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def logout(request):
    auth.logout(request)
    return shortcuts.redirect('home')

@cache.never_cache
def login(request):
    auth.logout(request)
    redirect_to = request.POST.get('next', request.GET.get('next', '/'))
    redirect_to = (redirect_to
                   if http.is_safe_url(redirect_to, request.get_host())
                   else '/')
    form = forms.AuthForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            auth.login(request, form.user)
            if not form.cleaned_data['remember']:
                request.session.set_expiry(0)
            return shortcuts.redirect(redirect_to)
    return shortcuts.render(request, 'accounts/login.html', {'next': redirect_to, 'form':form})

def home(request):
    return shortcuts.render(request, 'home.html', {'user': request.user})

def register(request):
    return shortcuts.render(request, 'accounts/register.html')

def accountList(request):
    account_list = Account.objects.all()
    if 'q' in request.GET:
        account_list=account_list.filter(name__icontains=request.get['q'])

    page = request.GET.get('page', 1)

    paginator = Paginator(account_list, 10)
    try:
        accounts = paginator.page(page)
    except PageNotAnInteger:
        accounts = paginator.page(1)
    except EmptyPage:
        accounts = paginator.page(paginator.num_pages)

    return shortcuts.render(request, 'accounts/List.html', {'model':Account, 'instances':accounts})

def accountDetail(request, id):
    show=False
    account = shortcuts.get_object_or_404(Account,usafa_id=id)
    form = forms.accountEdit(instance=account)
    if request.method=='POST':
        form = forms.accountEdit(request.POST, instance=account)
        if form.is_valid():
            form.save()
        else:
            show=True
    return shortcuts.render(request, 'accounts/Detail.html',{'model':Account,'instance': account, 'form':form, 'show':show})