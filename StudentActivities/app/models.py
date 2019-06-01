from django.db import models
from django.db.models import F
from django.db.models import Count

# Create your models here.

class User(models.Model):
    user = models.CharField(u'管理员用户名', max_length=32, primary_key=True)
    passwd = models.CharField(u'管理员密码', max_length=64)
    priority = models.IntegerField(help_text=u'权限，0超级管理员，1普通管理员')
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    token = models.CharField(u'登陆验证', max_length=128)

class Activity(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.TextField(u'网页标题')
    content = models.TextField(u'活动简介')
    organizer = models.TextField(u'活动主办方')
    phone = models.CharField(u'主办方电话', max_length=16)
    address = models.TextField(u'主办方地址')
    convener = models.TextField(u'活动召集人')
    detail = models.TextField(u'活动详情')
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    start_time = models.DateTimeField(u'活动开始时间')
    end_time = models.DateTimeField(u'活动结束时间')
    price1 = models.CharField(u'团购价1', max_length=16)
    price2 = models.CharField(u'团购价2', max_length=16)
    price3 = models.CharField(u'团购价3', max_length=16)
    head_img = models.CharField(u'页面头活动海报', max_length=128)
    tail_img = models.CharField(u'页面尾活动海报', max_length=128)
    organizer_qrcode = models.CharField(u'主办方二维码', max_length=128)
    leader_qrcode_bg = models.CharField(u'团二维码海报模板', max_length=128)

class Student(models.Model):
    id = models.AutoField(primary_key=True)
    gid = models.IntegerField(help_text=u'组id')
    phone = models.CharField(u'联系电话', max_length=16)
    child_name = models.CharField(u'学员姓名', max_length=32)
    name = models.CharField(u'家长姓名', max_length=32)
    age = models.IntegerField(help_text=u'年龄')
    activity_id = models.IntegerField(help_text=u'活动id')
    course_id = models.IntegerField(help_text=u'课程id')
    status = models.IntegerField(help_text=u'0新生，1老生')
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    qr_code = models.CharField(u'团二维码', max_length=128)

class LoginLog(models.Model):
    user = models.CharField(u'管理员用户名', max_length=32)
    ip = models.CharField(u'登录ip', max_length=24)
    position = models.CharField(u'登录位置', max_length=24)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)

class Course(models.Model):
    id = models.AutoField(primary_key=True)
    activity_id = models.IntegerField(help_text=u'活动id')
    content = models.TextField(u'课程简介')