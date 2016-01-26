from __future__ import absolute_import

from django.shortcuts import render
from django.db.models import Count

from apps.repository.models import Repository


# Create your views here.



def main_page(request):
    dark_theme = True
    if request.user.is_authenticated():
        dark_theme = False
    repository_list = Repository.objects.annotate(num_star=Count('star')).order_by('-num_star')
    return render(request, 'main/main_page.html', {'dark_theme': dark_theme, 'repository_list': repository_list})
