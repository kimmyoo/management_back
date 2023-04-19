from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('id', 'username', 'email', 'is_superuser')
# admin.site.register(User, UserAdmin)

class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'is_superuser')
admin.site.register(User, CustomUserAdmin)