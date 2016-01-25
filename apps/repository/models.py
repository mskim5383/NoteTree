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
    meta_data = models.TextField(default='', max_length=200)


    def __str__(self):
        return 'Commit: %s/%s/%s/%d' % (self.branch.repository.userprofile.user.username, self.branch.repository.name, self.branch.name, self.id)

    def clone(self):
        commit = Commit()
        commit.branch = self.branch
        commit.meta_data = self.meta_data
        commit.save()
        for part in self.part.all():
            p = part.clone()
            part.commit = commit
            part.save()
        return commit

    def abc(self):
        ret = self.meta_data + '\n'
        ret2 = ""
        for part in self.part.order_by('order'):
            ret += part.meta_data + '\n'
            ret2 += part.notes + '\n'
        return ret + ret2


class Part(models.Model):
    commit = models.ForeignKey('Commit',
                                null=False, related_name='part')
    order = models.IntegerField(default=-1)
    meta_data = models.TextField(default='', max_length=200)
    notes = models.TextField(default='', max_length=10000)

    def clone(self):
        part = Part()
        part.order = self.order
        part.meta_data = self.meta_data
        part.notes = self.notes
        return part

