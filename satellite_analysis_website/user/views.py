from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.hashers import make_password, check_password
from .models import User


def user_login(request):
    print(request.session.get('user_id', -1))
    if request.session.get('user_id', -1) != -1:
        return HttpResponseRedirect('/analysis')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return HttpResponse('Login failed')

        if user and check_password(password, user.password):
            request.session['user_id'] = user.id
            return HttpResponseRedirect('/analysis')
        else:
            return HttpResponse('Login failed')

    request.session['user_id'] = -1
    return render(request, 'login.html')


def user_logout(request):
    request.session['user_id'] = -1
    return redirect('login')


def user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            hashed_password = make_password(password)
            user = User.objects.create(username=username, password=hashed_password)
            user.save()
            return HttpResponseRedirect('/user/login')
        else:
            return HttpResponse('Registration failed')

    request.session['user_id'] = -1
    return render(request, 'register.html')
