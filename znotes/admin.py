from django.contrib import admin

from . import models
from django.contrib.auth.models import Group,User
admin.site.unregister(Group)

admin.site.register(models.Note)
# admin.site.register(models.Profile)
admin.site.register(models.Department)
admin.site.register(models.MyFile)


class ProfileInline(admin.StackedInline):
    model = models.Profile

class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username"]
    inlines = [ProfileInline]

admin.site.unregister(User)
admin.site.register(User,UserAdmin)