from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from .forms import usersignup,userupdate,profileupdate
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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

@login_required
def profile(request):
    if(request.method=='POST'):
        u_form = userupdate(request.POST,instance = request.user)
        p_form = profileupdate(request.POST,request.FILES,instance = request.user.profile)
        if(u_form.is_valid() and p_form.is_valid()):
            u_form.save()
            p_form.save()
            messages.success(request,f'Your account has been Updated')
            return redirect('profile')
    else:
        u_form = userupdate(instance = request.user)
        p_form = profileupdate(instance = request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request,'accounts/profile.html',context)