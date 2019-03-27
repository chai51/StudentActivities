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

def queryLeaders():
    models.User.objects.filter(gid=request.POST['user']).values()