from __future__ import absolute_import

from django.shortcuts import render, redirect
from django.http import Http404

from apps.session.models import UserProfile
from apps.repository.models import Repository
from apps.repository.forms import RepositoryForm, BranchForm, CommitForm

# Create your views here.



def userprofile(request, username):
    userprofile = validity_check(username)
    return render(request, 'repository/userprofile.html',
                    {'userprofile': userprofile})


def repository(request, username, repo_name):
    userprofile, repository = validity_check(username, repo_name)
    return render(request, 'repository/repository.html',
                    {'repository': repository})

def create_repository(request, username):
    userprofile = validity_check(username)
    if userprofile != request.user.userprofile:
        raise Http404
    if request.method == 'POST':
        repository_form = RepositoryForm(request.POST, userprofile=userprofile)
        if repository_form.is_valid():
            repository = repository_form.save()
            return redirect('../' + repository.name)
    else:
        repository_form = RepositoryForm()
    return render(request, 'repository/create_repository.html',
                    {'repository_form': repository_form})

def branch(request, username, repo_name, branch_name):
    userprofile, repository, branch = validity_check(username, repo_name, branch_name)
    return render(request, 'repository/branch.html',
                    {'branch': branch})

def create_branch(request, username, repo_name):
    userprofile, repository = validity_check(username, repo_name)
    if userprofile != request.user.userprofile:
        raise Http404
    if request.method == 'POST':
        branch_form = BranchForm(request.POST, repository=repository)
        if branch_form.is_valid():
            branch = branch_form.save()
            return redirect('../' + branch.name)
    else:
        branch_form = BranchForm()
    return render(request, 'repository/create_branch.html',
                    {'branch_form': branch_form})

def commit(request, username, repo_name, branch_name, commit_id):
    try:
        commit_id = int(commit_id)
    except ValueError:
        raise Http404
    userprofile, repository, branch, commit = validity_check(username, repo_name, branch_name, commit_id)
    if request.method == 'POST':
        commit_form = CommitForm(request.POST, branch=branch)
        if commit_form.is_valid():
            commit = commit_form.save()
            return redirect('../' + str(commit.id))
    else:
        commit_form = CommitForm(initial={'meta_data': commit.meta_data})
    return render(request, 'repository/commit.html',
                    {'commit': commit, 'commit_form': commit_form})






def validity_check(username=None, repo_name=None, branch_name=None, commit_id=None):
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
    if branch_name is None:
        return (userprofile, repository)
    if not repository.branch.filter(name=branch_name).exists():
        raise Http404
    branch = repository.branch.get(name=branch_name)
    if commit_id is None:
        return (userprofile, repository, branch)
    if not branch.commit.filter(id=commit_id).exists():
        raise Http404
    commit = branch.commit.get(id=commit_id)
    return (userprofile, repository, branch, commit)
