from django.shortcuts import render

# Create your views here.



def main_page(request):
    dark_theme = True
    if request.user.is_authenticated():
        dark_theme = False
    return render(request, 'main/main_page.html', {'dark_theme': dark_theme})
