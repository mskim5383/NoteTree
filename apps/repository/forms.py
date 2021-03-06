from __future__ import absolute_import

from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms

from apps.repository.models import Repository, Branch, Commit, Part, Contributor
from apps.session.models import UserProfile



class RepositoryForm(ModelForm):
    class Meta:
        model = Repository
        exclude = ['userprofile']


    def __init__(self, *args, **kwargs):
        self.userprofile = kwargs.pop('userprofile', None)
        super(RepositoryForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.instance.userprofile = self.userprofile
        super(RepositoryForm, self).save(*args, **kwargs)
        master_branch = Branch()
        master_branch.name = 'master'
        master_branch.repository = self.instance
        master_branch.save()
        commit = Commit()
        commit.branch = master_branch
        commit.message = 'Initial Commit'
        commit.meta_data = "X: 1\nT: %s\nL:1/4\nK:G\n" % self.instance.name
        commit.userprofile = self.userprofile
        commit.save()
        contributor = Contributor()
        contributor.userprofile = self.userprofile
        contributor.repository = self.instance
        contributor.save()
        return self.instance

    def clean(self):
        cleaned_data = super(RepositoryForm, self).clean()
        if 'name' in cleaned_data:
            name = cleaned_data['name']
            if Repository.objects.filter(userprofile=self.userprofile, name=name).exists():
                self.add_error('name', 'already exist')
        return cleaned_data

class BranchForm(ModelForm):
    class Meta:
        model = Branch
        exclude = ['repository']


    def __init__(self, *args, **kwargs):
        self.repository = kwargs.pop('repository', None)
        super(BranchForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        userprofile = kwargs.pop('userprofile', None)
        self.instance.repository = self.repository
        super(BranchForm, self).save(*args, **kwargs)
        master_branch = self.repository.branch.get(name='master')
        head_commit = master_branch.commit.last().clone(userprofile)
        head_commit.branch = self.instance
        head_commit.userprofile = userprofile
        head_commit.save()
        return self.instance

    def clean(self):
        cleaned_data = super(BranchForm, self).clean()
        if 'name' in cleaned_data:
            name = cleaned_data['name']
            if Branch.objects.filter(repository=self.repository, name=name).exists():
                self.add_error('name', 'already exist')
        return cleaned_data

class CommitForm(ModelForm):
    class Meta:
        model = Commit
        exclude = ['branch', 'userprofile']


    def __init__(self, *args, **kwargs):
        self.branch = kwargs.pop('branch', None)
        self.userprofile = kwargs.pop('userprofile', None)
        super(CommitForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.instance.branch = self.branch
        self.instance.userprofile = self.userprofile
        super(CommitForm, self).save(*args, **kwargs)
        return self.instance


class ContributorForm(ModelForm):
    username = forms.CharField(max_length=20)

    class Meta:
        model = Contributor
        exclude = ['repository', 'userprofile']


    def __init__(self, *args, **kwargs):
        self.repository = kwargs.pop('repository', None)
        super(ContributorForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.instance.repository = self.repository
        super(ContributorForm, self).save(*args, **kwargs)
        return self.instance

    def clean(self):
        cleaned_data = super(ModelForm, self).clean()
        if 'username' in cleaned_data:
            username = cleaned_data['username']
            if UserProfile.objects.filter(user__username=username).exists():
                self.instance.userprofile = UserProfile.objects.get(user__username=username)
                if self.repository.is_valid(self.instance.userprofile):
                    self.add_error('username', 'aleary added')
            else:
                self.add_error('username', 'not exists')
        return cleaned_data



