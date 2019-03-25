from django.shortcuts import render
from . import models

# Create your views here.

def login(request):
    return render(request, 'login.html')

def login2(request):
    if request.method == 'POST':
        vals = models.User.objects.filter(request.POST['user'])
        print ("query " + vals)
        return render(request, 'index.html')

def index(request):
    return render(request, 'index.html')
