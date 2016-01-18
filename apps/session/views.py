from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from models import UserProfile
from django.contrib.auth.decorators import login_required



def user_login(request):
    if request.method == 'POST' and request.user is None:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(request, user)
            return redirect(request.POST.get('next', '/'))
        else:
            return render(request, 'session/login.html',
                          {'error': 'Invalid login',
                           'next': request.POST.get('next', '/')})
    return render(request, 'session/login.html',
                    {'next': request.GET.get('next', '/')})


def user_logout(request):
    if request.user.is_authenticated():
        logout(request)
    return redirect('/session/login')


