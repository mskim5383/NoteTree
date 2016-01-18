from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class UserProfile(models.Model):
    user = models.OneToOneField(User,
                                primary_key=True, related_name='userprofile')


    def __str__(self):
        return "User %s's profile object" % (self.user)
