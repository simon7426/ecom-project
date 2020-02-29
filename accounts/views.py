from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from .forms import usersignup
from django.contrib import messages

def signup(request):
    if(request.method=="POST"):
        form = usersignup(request.POST)
        if(form.is_valid()):
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Your account has been created! You can now Sign In')
            return redirect('login')

    else:
        form = usersignup()
    return render(request,'accounts/signup.html',{'form':form})

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

