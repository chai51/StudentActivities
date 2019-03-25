from django.db import models

# Create your models here.

class User(models.Model):
    user = models.CharField(u'管理员用户名', max_length=32, primary_key=True)
    passwd = models.CharField(u'管理员密码', max_length=64)
    priority = models.IntegerField(u'权限，0超级管理员，1普通管理员')
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)

class Event(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.TextField(u'标题')
    content = models.TextField(u'内容')
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)

class Student(models.Model):
    id = models.AutoField(primary_key=True)
    gid = models.IntegerField(u'组id')
    phone = models.CharField(u'联系电话', max_length=16)
    child_name = models.CharField(u'学员姓名', max_length=32)
    name = models.CharField(u'家长姓名', max_length=32)
    age = models.IntegerField(help_text=u'年龄')
    event_id = models.IntegerField(u'活动id')
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)

class LoginLog(models.Model):
    user = models.CharField(u'管理员用户名', max_length=32)
    ip = models.CharField(u'登录ip', max_length=24)
    position = models.CharField(u'登录位置', max_length=24)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)