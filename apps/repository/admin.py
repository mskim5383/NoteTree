from django.contrib import admin
from models import Repository, Branch, Movement, Part


# Register your models here.
admin.site.register(Repository)
admin.site.register(Branch)
admin.site.register(Movement)
admin.site.register(Part)
