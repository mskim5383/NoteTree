from __future__ import absolute_import

from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404

from apps.session.models import UserProfile
from apps.repository.models import Repository, Part, Star
from apps.repository.forms import RepositoryForm, BranchForm, CommitForm, ContributorForm

import json

# Create your views here.



def userprofile(request, username):
    userprofile = validity_check(username)
    contributor = userprofile.contributor.all()
    return render(request, 'repository/userprofile.html',
            {'userprofile': userprofile, 'contributor': contributor})


def repository(request, username, repo_name):
    userprofile, repository = validity_check(username, repo_name)
    master = repository.branch.get(name='master')
    star = repository.get_star(userprofile)
    return render(request, 'repository/repository.html',
            {'repository': repository, 'branch': master, 'star': star})

def create_repository(request, username):
    if not request.user.is_authenticated():
        raise Http404
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

def manage_repository(request, username, repo_name):
    if not request.user.is_authenticated():
        raise Http404
    userprofile, repository = validity_check(username, repo_name)
    if userprofile != request.user.userprofile:
        raise Http404
    if request.method == 'POST':
        contributor_form = ContributorForm(request.POST, repository=repository)
        if contributor_form.is_valid():
            contributor = contributor_form.save()
            return redirect('./')
    else:
        contributor_form = ContributorForm()
    return render(request, 'repository/manage_repository.html',
            {'repository': repository, 'contributor_form': contributor_form})

def search_repository(request):
    keyword = request.GET.get('keyword', '')
    repository_list = Repository.objects.filter(name__contains=keyword)
    return render(request, 'repository/search.html',
            {'repository_list': repository_list, 'keyword': keyword})

def star(request, username, repo_name):
    result = {'status': 'bad'}
    userprofile, repository = validity_check(username, repo_name)
    if request.method == 'POST':
        if Star.objects.filter(userprofile=request.user.userprofile, repository=repository).exists():
            star = Star.objects.get(userprofile=request.user.userprofile, repository=repository)
            star.delete()
            result = {'status': 'unstar'}
        else:
            star = Star()
            star.userprofile = request.user.userprofile
            star.repository = repository
            star.save()
            result = {'status': 'star'}
    return HttpResponse(json.dumps(result), content_type="application/json")


def branch(request, username, repo_name, branch_name):
    userprofile, repository, branch = validity_check(username, repo_name, branch_name)
    star = repository.get_star(userprofile)
    return render(request, 'repository/branch_main.html',
            {'branch': branch, 'star': star})

def create_branch(request, username, repo_name):
    if not request.user.is_authenticated():
        raise Http404
    userprofile, repository = validity_check(username, repo_name)
    if not repository.is_valid(request.user.userprofile):
        raise Http404
    if request.method == 'POST':
        branch_form = BranchForm(request.POST, repository=repository)
        if branch_form.is_valid():
            branch = branch_form.save(userprofile=request.user.userprofile)
            return redirect('../' + branch.name)
    else:
        branch_form = BranchForm()
    return render(request, 'repository/create_branch.html',
                    {'branch_form': branch_form})

def list_commit(request, username, repo_name, branch_name):
    userprofile, repository, branch = validity_check(username, repo_name, branch_name)
    star = repository.get_star(userprofile)
    return render(request, 'repository/list_commit.html',
            {'branch': branch, 'star': star})


def commit(request, username, repo_name, branch_name, commit_id):
    try:
        commit_id = int(commit_id)
    except ValueError:
        raise Http404
    userprofile, repository, branch, commit = validity_check(username, repo_name, branch_name, commit_id)
    if request.method == 'POST':
        if not request.user.is_authenticated():
            raise Http404
        if not repository.is_valid(request.user.userprofile):
            raise Http404
        commit_form = CommitForm(request.POST, branch=branch, userprofile=request.user.userprofile)
        if commit_form.is_valid():
            commit = commit_form.save()
            try:
                part_count = int(request.POST.get("part-count", 0))
            except ValueError:
                part_count = 0
            for i in range(part_count):
                try:
                    part_order = int(request.POST.get("part-order-" + str(i + 1)))
                    part_clef = request.POST.get("part-clef-" + str(i + 1), "treble")
                    part_name = request.POST.get("part-name-" + str(i + 1), "")
                    part_notes = request.POST.get("part-notes-" + str(i + 1), "")
                    part_deleted = int(request.POST.get("part-deleted-" + str(i + 1)))
                except:
                    continue
                if part_deleted == 0:
                    part = Part()
                    part.commit = commit
                    part.order = part_order
                    part.clef = part_clef
                    part.name = part_name
                    part.notes = part_notes
                    part.save()

            return redirect('../')
    else:
        commit_form = CommitForm(initial={'title': commit.title, 'meter': commit.meter, 'key': commit.key})
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
