from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from authenticator.models import FrontAuth, AuthLogs
from authenticator.forms import AuthenticatorForm, AddUserForm
from . import forms
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response

@login_required
def indexRedirect(request):
    response = HttpResponse("This is Index Bro!")
    return response

@login_required
def addUser(request):

    registered = False
    if request.user.is_superuser:
        if request.method == "POST":
            user_Form= AddUserForm(data=request.POST)
            if user_Form.is_valid():
                new_user= user_Form.save()
                new_user.set_password(new_user.password)
                print(new_user.username.split(".")[0],new_user.username.split(".")[1])
                new_user.first_name = new_user.username.split(".")[0]
                new_user.last_name = new_user.username.split(".")[1]
                new_user.save()
                return HttpResponseRedirect('/VISCAuth/login/')
            else:
                return HttpResponse("Form Invalid!")
        else:
            authForm = forms.AuthenticatorForm()
            server_info = {
                'server_name': "BEAST",
                'Form': authForm
            }
            return render(request, 'addUser.html', context=server_info)
    else :
        return HttpResponse("Only super User can add Users")

def loginAuth(request):
    authForm = forms.AuthenticatorForm()
    server_info={
        'server_name': "BEAST",
        'Form':authForm
                 }
    next_url = request.GET.get('next')
    if request.method == 'GET':
         return render(request, 'auth.html', context=server_info)

    if request.method == 'POST':
        username = request.POST.get('Uname')
        password = request.POST.get('hashKey')
        user= authenticate(username=username,password=password)
        authLog= AuthLogs(username=username,access_time=datetime.now(),authStat=(True if user else False))
        authLog.save()
        if user:
            if user.is_active:
                login(request,user)
                if next_url:
                    return HttpResponseRedirect(next_url)
                else:
                    return HttpResponseRedirect('/login_check/')
            else:
                return HttpResponse("Account Disabled!")

        else:
            return HttpResponse("User Account Error Contact Admin!")



@login_required
def logoutAuth(request):
    logout(request)
    return HttpResponseRedirect('/VISCAuth/login/')


def logincheck(request):
    if request.user.is_authenticated:
        return HttpResponse("Awesome You are Logged in!")
    else:
        return HttpResponse("Not Logged in Yet!")

@login_required
def serverRoot(request):
    response= HttpResponse()
    response['X-Accel-Redirect'] ='/beast'+request.path
    return response
