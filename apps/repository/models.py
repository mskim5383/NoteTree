from __future__ import unicode_literals

from django.db import models

# Create your models here.



class Repository(models.Model):
    name = models.CharField(max_length=20, null=False, default='')
    userprofile = models.ForeignKey('session.UserProfile',
                                    null=False, related_name='repository')
    readme = models.TextField(default='', max_length=1000)


    def __str__(self):
        return '%s/%s' % (self.userprofile.user.username, self.name)

    def is_valid(self, userprofile):
        if self.contributor.filter(userprofile=userprofile).exists():
            return True
        return False

    def get_star(self, userprofile):
        if self.star.filter(userprofile=userprofile).exists():
            return True
        return False

    def updated_time(self):
        commit = Commit.objects.filter(branch__repository=self).reverse()[0]
        return commit.created_time


class Contributor(models.Model):
    userprofile = models.ForeignKey('session.UserProfile',
                                    null=False, related_name='contributor')
    repository = models.ForeignKey('Repository', null=False, related_name='contributor')

    def __str__(self):
        return 'Contributor: %s, %s' % (self.repository, self.userprofile)


class Branch(models.Model):
    name = models.CharField(max_length=20, null=False, default='')
    repository = models.ForeignKey('Repository',
                                null=False,  related_name='branch')


    def __str__(self):
        return 'Branch: %s/%s/%s' % (self.repository.userprofile.user.username, self.repository.name, self.name)


class Commit(models.Model):
    userprofile = models.ForeignKey('session.UserProfile',
                                    null=False, related_name='commit')
    branch = models.ForeignKey('Branch',
                                null=False, related_name='commit')
    title = models.CharField(default='', max_length=20)
    meter = models.CharField(default='4/4', max_length=10)
    key = models.CharField(default='C', max_length=5)
    message = models.CharField(default='', blank=False, max_length=30)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return 'Commit: %s/%s/%s/%d' % (self.branch.repository.userprofile.user.username, self.branch.repository.name, self.branch.name, self.id)

    def clone(self):
        commit = Commit()
        commit.branch = self.branch
        commit.title = self.title
        commit.meter = self.meter
        commit.key = self.key
        commit.message = self.message
        commit.save()
        for part in self.part.all():
            p = part.clone()
            part.commit = commit
            part.save()
        return commit

    def get_meta(self):
        return 'X: 1\nT: %s\nM: %s\nK: %s\n' % (self.title, self.meter, self.key)

    def abc(self):
        ret = self.get_meta()
        ret2 = ""
        for part in self.part.order_by('order'):
            ret += part.get_meta()
            ret2 += '[V: %d]%s\n' % (part.id, part.notes)
        return ret + ret2


class Part(models.Model):
    CLEF_CHOICES = (
            ('treble', 'treble'),
            ('alto', 'alto'),
            ('tenor', 'tenor'),
            ('bass', 'bass'))

    commit = models.ForeignKey('Commit',
                                null=False, related_name='part')
    order = models.IntegerField(default=-1)
    clef = models.CharField(default='treble', max_length=10, choices=CLEF_CHOICES)
    name = models.CharField(default='', max_length=20)
    notes = models.TextField(default='', max_length=10000)

    def clone(self):
        part = Part()
        part.order = self.order
        part.clef = self.clef
        part.name = self.name
        part.notes = self.notes
        return part

    def get_meta(self):
        return 'V: %d clef=%s name="%s"\n' % (self.id, self.clef, self.name)

    def abc(self):
        return '%s%s[V: %d]%s' % (self.commit.get_meta(), self.get_meta(), self.id, self.notes)


class Star(models.Model):
    userprofile = models.ForeignKey('session.UserProfile',
                                    null=False, related_name='star')
    repository = models.ForeignKey('Repository', null=False, related_name='star')

    def __str__(self):
        return 'Star: %s, %s' % (self.repository, self.userprofile)
