from django.contrib import admin
from . import models

class User(admin.ModelAdmin):
    list_display = ("username", )
    
admin.site.register(models.User, User)
admin.site.register(models.Email)