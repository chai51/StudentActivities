from django.test import TestCase
from . import models

# Create your tests here.

# 团长
def insertLeader(phone, child_name, name, age, event_id):
    leader = models.Student(phone=phone, child_name=child_name, name=name, age=age, event_id=event_id)
    leader.save()
    leader.gid = leader.id
    leader.save()

# 团员
def insertMember(phone, child_name, name, age, event_id, gid):
    member = models.Student(gid=gid, phone=phone, child_name=child_name, name=name, age=age, event_id=event_id)
    member.save()

# 查询团购进程以及团长信息
def queryLeaders(event_id):
    leaders = models.Student.objects.filter(event_id=event_id,gid=models.F("id")).order_by("gid").values()
    cnts = models.Student.objects.filter(event_id=event_id).order_by("gid").values("gid").annotate(cnt=models.Count("gid"))

    for i in range(0, len(leaders)):
        leaders[i]["count"] = cnts[i]["cnt"]
        leaders[i]["phone"] = leaders[i]["phone"][:3] + "****" + leaders[i]["phone"][7:]
    return leaders

# 查询一个团的详细信息
def queryLeader(gid):
    leader = models.Student.objects.filter(gid=gid).values()
    for i in range(0, len(leader)):
        leader[i]["phone"] = leader[i]["phone"][:3] + "****" + leader[i]["phone"][7:]
    return leader

def queryEvent(event_id):
    return models.Event.objects.filter(id=event_id).values()[0]

def queryEvents():
    return models.Event.objects.order_by("-id").values()