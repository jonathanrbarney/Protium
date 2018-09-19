from django.http import *
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .forms import *
from .tokens import account_activation_token
from django.utils.encoding import force_text
from django.views.decorators import csrf, cache
from django.utils import http

@csrf.csrf_protect
@cache.never_cache
def account_login(request):
    logout(request)
    redirect_to = request.POST.get('next', request.GET.get('next', '/'))
    redirect_to = (redirect_to
                   if http.is_safe_url(redirect_to, request.get_host())
                   else '/')
    form = AuthForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            login(request, form.user)
            if not form.cleaned_data['remember']:
                request.session.set_expiry(0)
            return redirect(redirect_to)
    return render(request, 'accounts/account_login.html', {'form': form,
                                                    'next': redirect_to})

def account_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


def signup(request):
    if request.method == 'POST':
        form = Account_Creation_Form(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            return redirect('home')
    else:
        form = Account_Creation_Form()
    return render(request, 'accounts/signup.html', {'form': form})

