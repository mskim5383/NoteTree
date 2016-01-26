from django.contrib import admin
from models import Repository, Branch, Part, Commit, Contributor


# Register your models here.
admin.site.register(Repository)
admin.site.register(Branch)
admin.site.register(Commit)
admin.site.register(Part)
admin.site.register(Contributor)
