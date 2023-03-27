from django.contrib import admin
from .models import Instructor, License


# Register your models here.
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'tel', 'email', 'address')

admin.site.register(Instructor, InstructorAdmin)

class LicenseAdmin(admin.ModelAdmin):
    list_display = ('licNum', 'program', 'instructor')

admin.site.register(License, LicenseAdmin)
