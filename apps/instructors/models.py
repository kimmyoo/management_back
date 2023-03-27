from django.db import models
from apps.programs.models import Program


class Instructor(models.Model):
    name = models.CharField(max_length=255)
    tel = models.CharField(max_length=255, blank=True)
    email = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=True)

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        self.address = self.address.lower()
        self.email = self.email.lower()
        return super(Instructor, self).save(*args, **kwargs)
    
    def __str__(self):
        return '%s' % self.name

class License(models.Model):
    # license Number will be the foreign key for Class object
    licNum = models.CharField(max_length=100, unique=True)
    # if program is delete, licenses associated with program will also be deleted
    program = models.ForeignKey(Program, related_name="licenses", on_delete=models.PROTECT)
    instructor = models.ForeignKey(Instructor, related_name="licenses", on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        self.licNum = self.licNum.lower()
        return super(License, self).save(*args, **kwargs)
    
    def __str__(self):
        return  '%s' % self.licNum