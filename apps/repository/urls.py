"""NoteTree URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
import os

urlpatterns = [
    url(r'^search/$', 'apps.repository.views.search_repository'),
    url(r'^([\w \[\]\.]+)/$', 'apps.repository.views.userprofile'),
    url(r'^([\w \[\]\.]+)/create_repository/$', 'apps.repository.views.create_repository'),
    url(r'^([\w \[\]\.]+)/([\w \[\]\.]+)/$', 'apps.repository.views.repository'),
    url(r'^([\w \[\]\.]+)/([\w \[\]\.]+)/star/$', 'apps.repository.views.star'),
    url(r'^([\w \[\]\.]+)/([\w \[\]\.]+)/manage/$', 'apps.repository.views.manage_repository'),
    url(r'^([\w \[\]\.]+)/([\w \[\]\.]+)/create_branch/$', 'apps.repository.views.create_branch'),
    url(r'^([\w \[\]\.]+)/([\w \[\]\.]+)/([\w \[\]\.]+)/$', 'apps.repository.views.branch'),
    url(r'^([\w \[\]\.]+)/([\w \[\]\.]+)/([\w \[\]\.]+)/commits/$', 'apps.repository.views.list_commit'),
    url(r'^([\w \[\]\.]+)/([\w \[\]\.]+)/([\w \[\]\.]+)/([\d]+)/$', 'apps.repository.views.commit'),

]
