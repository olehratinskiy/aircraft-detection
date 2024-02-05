from django.shortcuts import render
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from .models import User
from django.shortcuts import render, HttpResponseRedirect


def user_login(request):
    print(request.session.get('user_id', -1))
    if request.session.get('user_id', -1) != -1:
        return HttpResponseRedirect('/analysis')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.filter(username=username).first()
        except:
            return HttpResponse('Login failed')

        if user and user.password == password:
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

        if username != '' and password != '':
            user = User.create_user(username, password)
            user.save()
            return HttpResponseRedirect('/user/login')
        else:
            return HttpResponse('Registration failed')

    request.session['user_id'] = -1
    return render(request, 'register.html')
