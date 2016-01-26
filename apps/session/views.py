from __future__ import absolute_import

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.files import File

import StringIO
from PIL import Image, ImageOps
import hashlib
import os

from apps.session.models import UserProfile
from apps.session.forms import UserForm, UserProfileForm
from NoteTree.settings import UPLOAD_DIR


def user_login(request):
    if request.user.is_authenticated():
        return redirect('/')
    if request.method == 'POST' and not request.user.is_authenticated():
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(request, user)
            return redirect(request.POST.get('next', '/'))
        else:
            return render(request, 'session/login.html',
                          {'error': 'Invalid login',
                           'next': request.POST.get('next', '/')})
    return render(request, 'session/login.html',
                    {'next': request.GET.get('next', '/')})


def user_logout(request):
    if request.user.is_authenticated():
        logout(request)
    return redirect('/session/login')


def register(request):
    if request.user.is_authenticated():
        return redirect('/')
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        user_profile_form = UserProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and user_profile_form.is_valid():
            user = user_form.save()
            userprofile = user_profile_form.save(commit=False)
            userprofile.user = user
            userprofile.save()
            try:
                thumbnail = _handle_uploaded_image(request.FILES['thumbnail'], 300, 300)
                userprofile.thumbnail = thumbnail
                userprofile.save()
            except:
                pass
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return redirect('/' + user.username + '/')
    else:
        user_form = UserForm()
        user_profile_form = UserProfileForm()
    return render(request, 'session/register.html',
                    {'user_form': user_form,
                     'user_profile_form': user_profile_form})


def account(request):
    if not request.user.is_authenticated():
        return redirect('/')
    if request.method == 'POST':
        user_profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_profile_form.is_valid():
            userprofile = user_profile_form.save()
            try:
                thumbnail = _handle_uploaded_image(request.FILES['thumbnail'], 300, 300)
                userprofile.thumbnail = thumbnail
                userprofile.save()
            except:
                pass
            return redirect('./')
    else:
        user_profile_form = UserProfileForm(instance=request.user.userprofile)
    return render(request, 'session/account.html',
                    {'user_profile_form': user_profile_form})


def _handle_uploaded_image(i, x, y):
    # read image from InMemoryUploadedFile
    image_str = ""
    for c in i.chunks():
        image_str += c

    # create PIL Image instance
    imagefile  = StringIO.StringIO(image_str)
    image = Image.open(imagefile)

    # if not RGB, convert
    if image.mode not in ("L", "RGB"):
        image = image.convert("RGB")

    #get orginal image ratio
    img_ratio = float(image.size[0]) / image.size[1]

    # resize but constrain proportions?
    if x==0.0:
        x = y * img_ratio
    elif y==0.0:
        y = x / img_ratio

    # output file ratio
    resize_ratio = float(x) / y
    x = int(x); y = int(y)

    # get output with and height to do the first crop
    if(img_ratio > resize_ratio):
        output_width = x * image.size[1] / y
        output_height = image.size[1]
        originX = image.size[0] / 2 - output_width / 2
        originY = 0
    else:
        output_width = image.size[0]
        output_height = y * image.size[0] / x
        originX = 0
        originY = image.size[1] / 2 - output_height / 2

    #crop
    cropBox = (originX, originY, originX + output_width, originY + output_height)
    image = image.crop(cropBox)

    # resize (doing a thumb)
    image.thumbnail([x, y], Image.ANTIALIAS)

    # re-initialize imageFile and set a hash (unique filename)
    imagefile = StringIO.StringIO()
    filename = hashlib.md5(imagefile.getvalue()).hexdigest()+'.jpg'

    #save to disk
    imagefile = open(os.path.join(UPLOAD_DIR,filename), 'w')
    image.save(imagefile,'JPEG', quality=90)
    imagefile = open(os.path.join(UPLOAD_DIR,filename), 'r')
    content = File(imagefile)

    return content
