from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.db import models
from django.core.exceptions import ObjectDoesNotExist


def signup(request):
    if(request.method =='POST'):
        if(request.POST['password1']==request.POST['password2']):
            try:
                user = User.objects.get(username=request.POST['username'])
                return render(request,'accounts/signup.html', {'error':'Username Already Taken'})
            except User.DoesNotExist:
                user = User.objects.create_user(username=request.POST['username'],
                                                password=request.POST['password1'],
                                                email=request.POST['email'],
                                                first_name=request.POST['firstname'],
                                                last_name=request.POST['lastname'])
                user.profile.address = request.POST['address']
                user.profile.contact_no = request.POST['contact_no']
            auth.login(request,user)
            return redirect('home') 
        else:
            return render(request,'accounts/signup.html', {'error':'Passwords Didn\'t Match'})
    else:
        return render(request,'accounts/signup.html')

def login(request):
    if(request.method=='POST'):
        user = auth.authenticate(username=request.POST['username'],password=request.POST['password'])
        if(user is not None):
            auth.login(request,user)
            return redirect('home')
        else:
            return render(request,'accounts/login.html',{'error':'Username & Password Didn\'t match'})
    else:
        return render(request,'accounts/login.html')

def logout(request):
    if(request.method=='POST'):
        auth.logout(request)
        return render(request,'accounts/logout.html')

