from django.shortcuts import render
from . import models
from . import tests

# Create your views here.

def login(request):
    return render(request, 'login.html')

def login2(request):
    if request.method == 'POST':
        #print (str(models.User.objects.filter(user="chai").query))
        values = models.User.objects.filter(user=request.POST['user']).values()
        passwd = request.POST['passwd']

        #print ("query:{0} ,post:{1}".format(values[0]['passwd'], request.POST['passwd']))
        if (values[0]['passwd'] == request.POST['passwd']):
            pass
        else:
            print ("passwd error")
        tests.insertLeader("15971111111", "child", "pid", 25, 10)
        tests.insertMember("15971111111", "child", "pid", 25, 10, 1000)
        return render(request, 'index.html')

def index(request):
    return render(request, 'index.html')
