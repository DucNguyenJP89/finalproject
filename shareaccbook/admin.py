from django.contrib import admin

from .models import User, UserAccBook, AccBookItem, SharedUser

# Register your models here.
admin.site.register(User)
admin.site.register(UserAccBook)
admin.site.register(AccBookItem)
admin.site.register(SharedUser)