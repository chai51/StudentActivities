from django.http import JsonResponse
from django.conf import settings
import django
import os
import json
from . import models
from . import tests
import hashlib


# Create your views here.

def login(request):
    data = {"code": "2", "info":"wrong request method"}
    if request.method == 'POST':
        postBody = {}
        try:
            postBody = json.loads(request.body.decode())
        except json.decoder.JSONDecodeError:
            data = {"code": "3", "info":"JSON format is incorrect"}
            return JsonResponse(data, safe=False)

        user = postBody.get("user")
        passwd = postBody.get("passwd")
        if user is None or passwd is None:
            data = {"code": "3", "info":"Missing at least one parameter : user passwd"}
            return JsonResponse(data, safe=False)
        
        values = list(models.User.objects.filter(user=user).values())
        if len(values) == 0:
            data = {"code": "10", "info":"Username not found"}
            return JsonResponse(data, safe=False)
        
        passwd2 = values[0].pop("passwd")
        if (passwd2 == passwd):
            data = {"code": "1", "info":"", "data":values}
        else:
            data = {"code": "10", "info":"wrong username or password"}
    return JsonResponse(data, safe=False)

def activity(request):
    data = {"code": "2", "info":"wrong request method"}
    if request.method == 'GET':
        values = list(models.Activity.objects.order_by("-id").values())
        data = {"code": "1", "info":"", "data":values}
    return JsonResponse(data, safe=False)

def leaders(request):
    data = {"code": "2", "info":"wrong request method"}
    if request.method == 'GET':
        activity_id = request.GET.get('activity_id')
        if activity_id is None:
            data = {"code": "3", "info":"Missing at least one parameter : activity_id"}
            return JsonResponse(data, safe=False)
        
        values = list(models.Student.objects.filter(activity_id=activity_id,gid=models.F("id")).order_by("gid").values())
        values2 = list(models.Student.objects.filter(activity_id=activity_id).order_by("gid").values("gid").annotate(cnt=models.Count("gid")))
        # 将查询数据融合，设置电话号码部分不可见
        for i in range(0, len(values)):
            values[i]["count"] = values2[i]["cnt"]
            values[i]["phone"] = values[i]["phone"][:3] + "****" + values[i]["phone"][7:]
        
        data = {"code": "1", "info":"", "data":values}
    return JsonResponse(data, safe=False)

def members(request):
    data = {"code": "2", "info":"wrong request method"}
    if request.method == 'GET':
        gid = request.GET.get('gid')
        if gid is None:
            data = {"code": "3", "info":"Missing at least one parameter : gid"}
            return JsonResponse(data, safe=False)

        values = list(models.Student.objects.filter(gid=gid).values())
        # 设置电话号码部分不可见
        for i in range(0, len(values)):
            values[i]["phone"] = values[i]["phone"][:3] + "****" + values[i]["phone"][7:]
        data = {"code": "1", "info":"", "data":values}
    return JsonResponse(data, safe=False)

def course(request):
    data = {"code": "2", "info":"wrong request method"}
    if request.method == 'GET':
        activity_id = request.GET.get('activity_id')
        if activity_id is None:
            data = {"code": "3", "info":"Missing at least one parameter : activity_id"}
            return JsonResponse(data, safe=False)

        values = list(models.Course.objects.filter(activity_id=activity_id).values())
        data = {"code": "1", "info":"", "data":values}
    return JsonResponse(data, safe=False)

def createActivity(request):
    data = {"code": "2", "info":"wrong request method"}
    if request.method == 'POST':
        postBody = {}
        try:
            postBody = json.loads(request.body.decode())
        except json.decoder.JSONDecodeError:
            data = {"code": "3", "info":"JSON format is incorrect"}
            return JsonResponse(data, safe=False)

        activity = models.Activity()
        title = postBody.get("title")
        if not title is None:
            activity.title = title
        content = postBody.get("content")
        if not content is None:
            activity.content = content
        organizer = postBody.get("organizer")
        if not organizer is None:
            activity.organizer = organizer
        phone = postBody.get("phone")
        if not phone is None:
            activity.phone = phone        
        address = postBody.get("address")
        if not address is None:
            activity.address = address        
        convener = postBody.get("convener")
        if not convener is None:
            activity.convener = convener      
        detail = postBody.get("detail")
        if not detail is None:
            activity.detail = detail      
        start_time = postBody.get("start_time")
        if not start_time is None:
            activity.start_time = start_time
        end_time = postBody.get("end_time")
        if not end_time is None:
            activity.end_time = end_time
        price1 = postBody.get("price1")
        if not price1 is None:
            activity.price1 = price1
        price2 = postBody.get("price2")
        if not price2 is None:
            activity.price2 = price2    
        price3 = postBody.get("price3")
        if not price3 is None:
            activity.price3 = price3

        try:
            activity.save()
        except django.core.exceptions.ValidationError as e:
            data = {"code": "3", "info":"{}".format(e)}
            return JsonResponse(data, safe=False)

        data = {"code": "1", "info":"", "data":[{"id":activity.id}]}
    return JsonResponse(data, safe=False)

def updateActivity(request):
    data = {"code": "2", "info":"wrong request method"}
    if request.method == 'POST':
        postBody = {}
        try:
            postBody = json.loads(request.body.decode())
        except json.decoder.JSONDecodeError:
            data = {"code": "3", "info":"JSON format is incorrect"}
            return JsonResponse(data, safe=False)

        activity_id = postBody.get('activity_id')
        if activity_id is None:
            data = {"code": "3", "info":"Missing at least one parameter : activity_id"}
            return JsonResponse(data, safe=False)

        activity = models.Activity()
        try:
            activity = models.Activity.objects.get(id=activity_id)
        except models.Activity.DoesNotExist:
            data = {"code": "4", "info":"no data found"}
            return JsonResponse(data, safe=False)

        title = postBody.get("title")
        if not title is None:
            activity.title = title
        content = postBody.get("content")
        if not content is None:
            activity.content = content
        organizer = postBody.get("organizer")
        if not organizer is None:
            activity.organizer = organizer
        phone = postBody.get("phone")
        if not phone is None:
            activity.phone = phone        
        address = postBody.get("address")
        if not address is None:
            activity.address = address        
        convener = postBody.get("convener")
        if not convener is None:
            activity.convener = convener      
        detail = postBody.get("detail")
        if not detail is None:
            activity.detail = detail      
        start_time = postBody.get("start_time")
        if not start_time is None:
            activity.start_time = start_time      
        end_time = postBody.get("end_time")
        if not end_time is None:
            activity.end_time = end_time      
        price1 = postBody.get("price1")
        if not price1 is None:
            activity.price1 = price1
        price2 = postBody.get("price2")
        if not price2 is None:
            activity.price2 = price2    
        price3 = postBody.get("price3")
        if not price3 is None:
            activity.price3 = price3

        try:
            activity.save()
        except django.core.exceptions.ValidationError as e:
            data = {"code": "3", "info":"{}".format(e)}
            return JsonResponse(data, safe=False)

        data = {"code": "1", "info":""}
    return JsonResponse(data, safe=False)

def updateActivity2(request):
    data = {"code": "2", "info":"wrong request method"}
    if request.method == 'POST':
        activity_id = request.POST.get('activity_id')
        if activity_id is None:
            data = {"code": "3", "info":"Missing at least one parameter : activity_id"}
            return JsonResponse(data, safe=False)

        activity = models.Activity()
        try:
            activity = models.Activity.objects.get(id=activity_id)
        except models.Activity.DoesNotExist:
            data = {"code": "4", "info":"no data found"}
            return JsonResponse(data, safe=False)

        path = os.path.join(settings.STATIC_ROOT, str(activity.id))
        if os.path.exists(path) == False:
            os.makedirs(path)

        head_img = request.FILES.get('head_img')
        if not head_img is None:
            activity.head_img = os.path.join(path, head_img.name)
            fw = open(activity.head_img, 'wb')
            for chunk in head_img.chunks():
                fw.write(chunk)
            fw.close()
            newFile = os.path.join(path, "head_img.png")
            if activity.head_img != newFile:
                tests.convertImgFmt(activity.head_img, newFile)
                os.remove(activity.head_img)
            activity.head_img = tests.convertPath(newFile)

        tail_img = request.FILES.get('tail_img')
        if not tail_img is None:
            activity.tail_img = os.path.join(path, tail_img.name)
            fw = open(activity.tail_img, 'wb')
            for chunk in tail_img.chunks():
                fw.write(chunk)
            fw.close()
            newFile = os.path.join(path, "tail_img.png")
            if activity.tail_img != newFile:
                tests.convertImgFmt(activity.tail_img, newFile)
                os.remove(activity.tail_img)
            activity.tail_img = tests.convertPath(newFile)

        organizer_qrcode = request.FILES.get('organizer_qrcode')
        if not organizer_qrcode is None:
            activity.organizer_qrcode = os.path.join(path, organizer_qrcode.name)
            fw = open(activity.organizer_qrcode, 'wb')
            for chunk in organizer_qrcode.chunks():
                fw.write(chunk)
            fw.close()
            newFile = os.path.join(path, "organizer_qrcode.png")
            if activity.organizer_qrcode != newFile:
                tests.convertImgFmt(activity.organizer_qrcode, newFile)
                os.remove(activity.organizer_qrcode)
            activity.organizer_qrcode = tests.convertPath(newFile)

        leader_qrcode_bg = request.FILES.get('leader_qrcode_bg')
        if not leader_qrcode_bg is None:
            activity.leader_qrcode_bg = os.path.join(path, leader_qrcode_bg.name)
            fw = open(activity.leader_qrcode_bg, 'wb')
            for chunk in leader_qrcode_bg.chunks():
                fw.write(chunk)
            fw.close()
            newFile = os.path.join(path, "leader_qrcode_bg.png")
            if activity.leader_qrcode_bg != newFile:
                tests.convertImgFmt(activity.leader_qrcode_bg, newFile)
                os.remove(activity.leader_qrcode_bg)
            activity.leader_qrcode_bg = tests.convertPath(newFile)

        activity.save()
        data = {"code": "1", "info":"", "data":[{"head_img":activity.head_img, "tail_img":activity.tail_img, "organizer_qrcode":activity.organizer_qrcode, "leader_qrcode_bg":activity.leader_qrcode_bg}]}
    return JsonResponse(data, safe=False)

def createLeader(request):
    data = {"code": "2", "info":"wrong request method"}
    if request.method == 'POST':
        postBody = {}
        try:
            postBody = json.loads(request.body.decode())
        except json.decoder.JSONDecodeError:
            data = {"code": "3", "info":"JSON format is incorrect"}
            return JsonResponse(data, safe=False)

        activity_id = postBody.get("activity_id")
        if activity_id is None:
            data = {"code": "3", "info":"Missing at least one parameter : activity_id"}
            return JsonResponse(data, safe=False)

        student = models.Student()
        student.activity_id = activity_id
        phone = postBody.get("phone")
        if not phone is None:
            student.phone = phone
        child_name = postBody.get("child_name")
        if not child_name is None:
            student.child_name = child_name
        name = postBody.get("name")
        if not name is None:
            student.name = name
        age = postBody.get("age")
        if not age is None:
            student.age = age
        course_id = postBody.get("course_id")
        if not course_id is None:
            student.course_id = course_id
        status = postBody.get("status")
        if not status is None:
            student.status = status
        student.save()

        student.gid = student.id

        urlQRCode = "activity_id={}&gid={}".format(student.activity_id, student.gid)
        pathQRCode = os.path.join(settings.STATIC_ROOT, str(student.activity_id), str(student.gid)+".png")
        tests.createQRCodeEx(
            os.path.join(settings.STATIC_ROOT, str(student.activity_id), "leader_qrcode_bg.png"),
            name,
            "邀请你一起来报课",
            urlQRCode,
            pathQRCode
        )

        student.qr_code = tests.convertPath(pathQRCode)
        student.save()

        data = {"code": "1", "info":"", "data":[{"id":student.id, "gid":student.gid, "qr_code":student.qr_code}]}
    return JsonResponse(data, safe=False)

def joinLeader(request):
    data = {"code": "2", "info":"wrong request method"}
    if request.method == 'POST':
        postBody = {}
        try:
            postBody = json.loads(request.body.decode())
        except json.decoder.JSONDecodeError:
            data = {"code": "3", "info":"JSON format is incorrect"}
            return JsonResponse(data, safe=False)

        activity_id = postBody.get("activity_id")
        gid = postBody.get("gid")
        if activity_id is None or gid is None:
            data = {"code": "3", "info":"Missing at least one parameter : activity_id gid"}
            return JsonResponse(data, safe=False)

        student = models.Student()
        student.activity_id = activity_id
        student.gid = gid
        phone = postBody.get("phone")
        if not phone is None:
            student.phone = phone
        child_name = postBody.get("child_name")
        if not child_name is None:
            student.child_name = child_name
        name = postBody.get("name")
        if not name is None:
            student.name = name
        age = postBody.get("age")
        if not age is None:
            student.age = age
        course_id = postBody.get("course_id")
        if not course_id is None:
            student.course_id = course_id
        status = postBody.get("status")
        if not status is None:
            student.status = status
        student.save()


        data = {"code": "1", "info":"", "data":[{"id":student.id}]}
    return JsonResponse(data, safe=False)

def createCourse(request):
    data = {"code": "2", "info":"wrong request method"}
    if request.method == 'POST':
        postBody = {}
        try:
            postBody = json.loads(request.body.decode())
        except json.decoder.JSONDecodeError:
            data = {"code": "3", "info":"JSON format is incorrect"}
            return JsonResponse(data, safe=False)

        activity_id = postBody.get("activity_id")
        if activity_id is None:
            data = {"code": "3", "info":"Missing at least one parameter : activity_id"}
            return JsonResponse(data, safe=False)

        course = models.Course()
        course.activity_id = activity_id
        content = postBody.get("content")
        if not content is None:
            course.content = content
        course.save()

        data = {"code": "1", "info":"", "data":[{"id":course.id}]}
    return JsonResponse(data, safe=False)

def updateCourse(request):
    data = {"code": "2", "info":"wrong request method"}
    if request.method == 'POST':
        postBody = {}
        try:
            postBody = json.loads(request.body.decode())
        except json.decoder.JSONDecodeError:
            data = {"code": "3", "info":"JSON format is incorrect"}
            return JsonResponse(data, safe=False)

        course_id = postBody.get("course_id")
        if course_id is None:
            data = {"code": "3", "info":"Missing at least one parameter : course_id"}
            return JsonResponse(data, safe=False)

        course = models.Course()
        try:
            course = models.Course.objects.get(id=course_id)
        except models.Course.DoesNotExist:
            data = {"code": "4", "info":"no data found"}
            return JsonResponse(data, safe=False)

        content = postBody.get("content")
        if not content is None:
            course.content = content
        course.save()

        data = {"code": "1", "info":""}
    return JsonResponse(data, safe=False)

def deleteCourse(request):
    data = {"code": "2", "info":"wrong request method"}
    if request.method == 'POST':
        postBody = {}
        try:
            postBody = json.loads(request.body.decode())
        except json.decoder.JSONDecodeError:
            data = {"code": "3", "info":"JSON format is incorrect"}
            return JsonResponse(data, safe=False)

        course_id = postBody.get("course_id")
        if course_id is None:
            data = {"code": "3", "info":"Missing at least one parameter : course_id"}
            return JsonResponse(data, safe=False)

        course = models.Course()
        try:
            course = models.Course.objects.get(id=course_id)
        except models.Course.DoesNotExist:
            data = {"code": "1", "info":""}
            return JsonResponse(data, safe=False)

        course.delete()
        data = {"code": "1", "info":""}
    return JsonResponse(data, safe=False)

def deleteMember(request):
    data = {"code": "2", "info":"wrong request method"}
    if request.method == 'POST':
        postBody = {}
        try:
            postBody = json.loads(request.body.decode())
        except json.decoder.JSONDecodeError:
            data = {"code": "3", "info":"JSON format is incorrect"}
            return JsonResponse(data, safe=False)

        uid = postBody.get("uid")
        if uid is None:
            data = {"code": "3", "info":"Missing at least one parameter : uid"}
            return JsonResponse(data, safe=False)

        student = models.Student()
        try:
            student = models.Student.objects.get(id=uid)
        except models.Student.DoesNotExist:
            data = {"code": "1", "info":""}
            return JsonResponse(data, safe=False)

        student.delete()
        data = {"code": "1", "info":""}
    return JsonResponse(data, safe=False)

def qrCode(request):
    data = {"code": "2", "info":"wrong request method"}
    if request.method == 'POST':
        postBody = {}
        try:
            postBody = json.loads(request.body.decode())
        except json.decoder.JSONDecodeError:
            data = {"code": "3", "info":"JSON format is incorrect"}
            return JsonResponse(data, safe=False)

        dataSrc = postBody.get("data")
        if dataSrc is None:
            data = {"code": "3", "info":"Missing at least one parameter : data"}
            return JsonResponse(data, safe=False)
        md5 = hashlib.md5()
        md5.update(dataSrc.encode("utf-8"))
        dataDst = md5.hexdigest()

        path = os.path.join(settings.STATIC_ROOT, "tmp")
        if os.path.exists(path) == False:
            os.makedirs(path)

        file = os.path.join(path, "{}.png".format(dataDst))
        if os.path.exists(file) == False:
            tests.createQRCode(dataSrc, file)
        data = {"code": "1", "info":"", "data":[{"qr_code":tests.convertPath(file)}]}
    return JsonResponse(data, safe=False)

def test(request):
    return JsonResponse({"code":"1", "info":"test"}, safe=False)