from django.contrib import admin

from .models import User, UserAccBook, AccBookItem

# Register your models here.
admin.site.register(User)
admin.site.register(UserAccBook)
admin.site.register(AccBookItem)