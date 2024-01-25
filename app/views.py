from django.shortcuts import render
from app.forms import *
from django.http import HttpResponse,HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
# Create your views here.
def registration(request):
    ufo=Userform()
    pfo=Profileform()
    d={'ufo':ufo,'pfo':pfo}
    if request.method=='POST' and request.FILES:
        ufd=Userform(request.POST)
        pfd=Profileform(request.POST,request.FILES)
        if ufd.is_valid() and pfd.is_valid():
            MUFDO=ufd.save(commit=False)
            pw=ufd.cleaned_data['password']
            MUFDO.set_password(pw)
            MUFDO.save()

            MPFDO=pfd.save(commit=False)
            MPFDO.username=MUFDO
            MPFDO.save()
            send_mail('registration',
                       'Thank you for registration',
                       'divyavani42000@gmail.com',
                       [MUFDO.email],
                       fail_silently=True)
            return HttpResponse('registration successfull')
        else:
            return HttpResponse('invalid data')

    return render(request,'registration.html',d)


def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)
    return render(request,'home.html')
def user_login(request):
    if request.method=='POST':
        username=request.POST['un']
        password=request.POST['pw']
        AUO=authenticate(username=username,password=password)
        if AUO and AUO.is_active:
            login(request,AUO)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse('invalid credentials')
        
    return render(request,'user_login.html')
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))
@login_required
def profile_display(request):
    un=request.session.get('username')
    UO=User.objects.get(username=un)
    PO=Profile.objects.get(username=UO)
    d={'UO':UO,'PO':PO}
    return render(request,'profile_display.html',d)
    