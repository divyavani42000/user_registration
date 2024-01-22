from django.shortcuts import render
from app.forms import *
from django.http import HttpResponse
from django.core.mail import send_mail
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