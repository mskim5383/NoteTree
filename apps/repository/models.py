from __future__ import unicode_literals

from django.db import models

# Create your models here.



class Repository(models.Model):
    userprofile = models.ForeignKey('session.UserProfile',
                                    null=False, related_name='repository')
    master_branch = models.OneToOneField('Branch',
                                    null=False, related_name='_repository')
    readme = models.TextField(default='', max_length=1000)


class Branch(models.Model):
    repository = models.ForeignKey('Repository',
                                null=False,  related_name='branch')
    head_commit = models.OneToOneField('Commit',
                                null=False, related_name='_branch')


class Commit(models.Model):
    branch = models.ForeignKey('Branch',
                                null=False, related_name='commit')


class Movement(models.Model):
    commit = models.ForeignKey('Commit',
                                null=False, related_name='movement')
    meta_data = models.TextField(default='', max_length=200)
    no = models.IntegerField(default=-1)


class Part(models.Model):
    order = models.IntegerField(default=-1)
    meta_data = models.TextField(default='', max_length=200)
    notes = models.TextField(default='', max_length=10000)

