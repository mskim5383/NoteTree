from __future__ import unicode_literals

from django.db import models

# Create your models here.



class Repository(models.Model):
    name = models.CharField(max_length=20, null=False, default='')
    userprofile = models.ForeignKey('session.UserProfile',
                                    null=False, related_name='repository')
    readme = models.TextField(default='', max_length=1000)


    def __str__(self):
        return 'Repository: %s/%s' % (self.userprofile.user.username, self.name)


class Branch(models.Model):
    name = models.CharField(max_length=20, null=False, default='')
    repository = models.ForeignKey('Repository',
                                null=False,  related_name='branch')


    def __str__(self):
        return 'Branch: %s/%s/%s' % (self.repository.userprofile.user.username, self.repository.name, self.name)


class Commit(models.Model):
    branch = models.ForeignKey('Branch',
                                null=False, related_name='commit')


class Movement(models.Model):
    name = models.CharField(max_length=20, null=False, default='')
    commit = models.ForeignKey('Commit',
                                null=False, related_name='movement')
    meta_data = models.TextField(default='', max_length=200)
    no = models.IntegerField(default=-1)


class Part(models.Model):
    order = models.IntegerField(default=-1)
    meta_data = models.TextField(default='', max_length=200)
    notes = models.TextField(default='', max_length=10000)

