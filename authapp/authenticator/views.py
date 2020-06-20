from datetime import datetime

from django.utils.decorators import method_decorator

from . import forms

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import requires_csrf_token, ensure_csrf_cookie, csrf_protect
from django.template.context_processors import csrf

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from authenticator import serializers
from authenticator import models
from authenticator.models import FrontAuth, AuthLogs
from authenticator.forms import AuthenticatorForm, AddUserForm


class CRSFObtainAuthToken(ObtainAuthToken):
    @classmethod
    def as_view(cls, **initkwargs):
        # Force enables CSRF protection.  This is needed for unauthenticated API endpoints
        # because DjangoRestFramework relies on SessionAuthentication for CSRF validation
        view = super().as_view(**initkwargs)
        view.csrf_exempt = False
        return view

class CRSFAPIView(APIView):
    @classmethod
    def as_view(cls, **initkwargs):
        # Force enables CSRF protection.  This is needed for unauthenticated API endpoints
        # because DjangoRestFramework relies on SessionAuthentication for CSRF validation
        view = super().as_view(**initkwargs)
        view.csrf_exempt = False
        return view




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

class CSRFToken(APIView):

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, format=None):
        """Sends a CSRF Token to use for Initial API call"""
        cont = {'Login': 'Your Login Token is Generated, Please use Wisely!'}
        print (cont)
        return JsonResponse(cont)


class UsersViewSet(viewsets.ModelViewSet):
    """Handles creating and updating users"""
    serializer_class = serializers.UserSerializer
    queryset = models.Users.objects.all()

class CreateUserView(generics.CreateAPIView):
    """ Create New User API"""
    serializer_class = serializers.UserSerializer



class CreateTokenView(CRSFObtainAuthToken):
    """ Create Auth Token"""
    serializer_class = serializers.AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class ManageUsersView(generics.RetrieveUpdateAPIView):
    """ Manage user API"""
    serializer_class = serializers.ManageUserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrive and return authd User"""
        return self.request.user


class CheckTokenView(APIView):
    """ Check if the Auth Token is valid and returns boolean"""
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request, format=None):
        return JsonResponse({'TokenValid': True})