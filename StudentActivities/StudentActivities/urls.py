"""StudentActivities URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from app import views as app_views

urlpatterns = [
    url(r'^login$', app_views.login),
    url(r'^activity$', app_views.activity),
    url(r'^leaders$', app_views.leaders),
    url(r'^members$', app_views.members),
    url(r'^course$', app_views.course),

    url(r'^createActivity$', app_views.createActivity),
    url(r'^updateActivity$', app_views.updateActivity),
    url(r'^updateActivity2$', app_views.updateActivity2),    
    url(r'^createLeader', app_views.createLeader),
    url(r'^joinLeader', app_views.joinLeader),
    url(r'^createCourse', app_views.createCourse),
    url(r'^updateCourse', app_views.updateCourse),
    url(r'^deleteCourse', app_views.deleteCourse),
    url(r'^deleteMember', app_views.deleteMember),

    url(r'^test$', app_views.test)
]
