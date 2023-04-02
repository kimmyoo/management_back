from django.contrib import admin
from .models import Class, Student

# Register your models here.
class ClassAdmin(admin.ModelAdmin):
    list_display = ('id', 'program', 'code', 'begin', 'end', 'schedule', 'status')
admin.site.register(Class, ClassAdmin)



class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'studentID', 'lName', 'fName', 'dob', 'last4Digits')
admin.site.register(Student, StudentAdmin)