from __future__ import absolute_import

from django.shortcuts import render
from django.http import Http404

from apps.session.models import UserProfile
from apps.repository.models import Repository

# Create your views here.



def userprofile(request, username):
    if not UserProfile.objects.filter(user__username=username).exists():
        raise Http404
    userprofile = UserProfile.objects.get(user__username=username)
    return render(request, 'repository/userprofile.html',
                    {'userprofile': userprofile})


def repository(request, username, repo_name):
    if not UserProfile.objects.filter(user__username=username).exists():
        raise Http404
    userprofile = UserProfile.objects.get(user__username=username)
    if not userprofile.repository.filter(name=repo_name).exists():
        raise Http404
    repository = userprofile.repository.get(name=repo_name)
    return render(request, 'repository/repository.html',
                    {'repository': repository})
