from django.shortcuts import render
from app.forms import *
# Create your views here.
def registration(request):
    ufo=Userform()
    pfo=Profileform()
    d={'ufo':ufo,'pfo':pfo}

    return render(request,'registration.html',d)