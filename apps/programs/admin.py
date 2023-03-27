from django.contrib import admin
from .models import Program



# Register your models here.
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('programName', 'programCode', 'length', 
                    'expiresAt', 'isActive', 'createdAt', 
                    'updatedAt')

admin.site.register(Program, ProgramAdmin)
