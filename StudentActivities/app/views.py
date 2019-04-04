from django.shortcuts import render
import os
from . import models
from . import tests
from StudentActivities import settings

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
            return render(request, 'login.html', {"error":"user or passwd error"})
        
        events = tests.queryEvents()
        print ("events:{0}".format(events))
        return render(request, 'index.html', {"events":events})

def activities(request):
    eventInfo = dict()
    if request.method == 'GET':
        event_id = request.GET['event_id']
        eventInfo = tests.queryEvent(event_id)

        gid = request.GET.get('gid')
        if gid is None:
            eventInfo["leaders"] = tests.queryLeaders(event_id)
            eventInfo["courses"] = tests.queryCourses(event_id)
        else:
            eventInfo["leader"] = tests.queryLeader(gid)
            eventInfo["count"] = len(eventInfo["leader"])
            eventInfo["courses"] = tests.queryCourses(event_id)

    print ("eventInfo:{0}".format(eventInfo))
    return render(request, 'activities{0}.html'.format(event_id), eventInfo)

def upload(request):
    if request.method == 'POST':
        obj = request.FILES.get('uploadfile')
        print ("file name:{0}".format(obj.name))
        path = os.path.join(settings.BASE_DIR, 'static', '1000')
        if os.path.exists(path) == False:
            os.makedirs(path)
        fw = open(os.path.join(path, obj.name), 'wb')
        for chunk in obj.chunks():
            fw.write(chunk)
        fw.close()
    return render(request, 'test.html')
        
def create(request):
    if request.method == 'POST':
        child_name = request.POST['kaiman']
        phone = request.POST['phone']
        age = request.POST['baomin0']
        name = request.POST['baomin1']
        select = request.POST['select']
        status = request.POST['radio1']
        event_id = request.POST['event_id']
        print ("child name:{}, phone:{}, age:{}, name:{}, select:{}, radio1:{}".format(child_name, phone, age, name, select, status))
        tests.insertLeader(phone, child_name, name, age, event_id, status, select)
    return render(request, 'test.html')

def join(request):
    if request.method == 'POST':
        child_name = request.POST['kaiman']
        phone = request.POST['phone']
        age = request.POST['baomin0']
        name = request.POST['baomin1']
        select = request.POST['select']
        status = request.POST['radio1']
        event_id = request.POST['event_id']
        gid = request.POST['gid']
        tests.insertMember(phone, child_name, name, age, event_id, gid, status, select)
    return render(request, 'test.html')
