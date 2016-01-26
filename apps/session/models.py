from __future__ import unicode_literals, absolute_import

from django.db import models
from django.contrib.auth.models import User

from NoteTree.settings import UPLOAD_DIR

# Create your models here.



class UserProfile(models.Model):
    user = models.OneToOneField(User,
                                primary_key=True, related_name='userprofile')
    name = models.CharField(default='', max_length=20)
    thumbnail = models.ImageField(null=True, blank=True, upload_to=UPLOAD_DIR)

    def get_thumbnail_url(self):
        if self.thumbnail:
            return '/upload/'+self.thumbnail.url.split('/')[-1]
        return '/media/default.jpg'

    def __str__(self):
        return "User %s's profile object" % (self.user)
