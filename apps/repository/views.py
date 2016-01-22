from __future__ import absolute_import

from django.shortcuts import render, redirect
from django.http import Http404

from apps.session.models import UserProfile
from apps.repository.models import Repository
from apps.repository.forms import RepositoryForm

# Create your views here.



def userprofile(request, username):
    userprofile = validity_check(username)
    return render(request, 'repository/userprofile.html',
                    {'userprofile': userprofile})


def repository(request, username, repo_name):
    repository = validity_check(username, repo_name)
    return render(request, 'repository/repository.html',
                    {'repository': repository})

def create_repository(request, username):
    userprofile = validity_check(username)
    if request.method == 'POST':
        repository_form = RepositoryForm(request.POST, userprofile=userprofile)
        if repository_form.is_valid():
            repository = repository_form.save()
            return redirect('../' + repository.name)
    else:
        repository_form = RepositoryForm()
    return render(request, 'repository/create_repository.html',
                    {'repository_form': repository_form})



def validity_check(username=None, repo_name=None):
    if username is None:
        return
    if not UserProfile.objects.filter(user__username=username).exists():
        raise Http404
    userprofile = UserProfile.objects.get(user__username=username)
    if repo_name is None:
        return userprofile
    if not userprofile.repository.filter(name=repo_name).exists():
        raise Http404
    repository = userprofile.repository.get(name=repo_name)
    return repository
