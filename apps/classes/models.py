from django.db import models
from apps.instructors.models import License
from apps.programs.models import Program

# Create your models here.
class Class(models.Model):
    # required
    program = models.ForeignKey(Program, related_name="classes", on_delete=models.PROTECT)
    license = models.ForeignKey(License, related_name="classes", on_delete=models.PROTECT)
    code = models.CharField(max_length=100, unique=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    # form can be blank; database can be null
    schedule = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    begin = models.DateField(max_length=100, blank=True, null=True)
    end = models.DateField(max_length=100, blank=True, null=True)
    intBegin = models.DateField(max_length=100, blank=True, null=True)
    intEnd = models.DateField(max_length=100, blank=True, null=True)
    intSite = models.CharField(max_length=255, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    
    
    def __str__(self):
        return self.code
    
    def save(self, *args, **kwargs):
        self.code = self.code.lower()
        if self.schedule:
            self.schedule = self.schedule.lower()
        if self.status:
            self.status = self.status.lower()
        if self.intSite:
            self.status = self.intSite.lower()
        if self.note:
            self.note = self.note.lower()
        return super(Class, self).save(*args, **kwargs)


# Create your models here.
class Student(models.Model):
    classes = models.ManyToManyField(Class, related_name="classes")
    # required fields
    studentID = models.CharField(max_length=30, unique=True)
    dob = models.DateField(max_length=15)
    lName = models.CharField(max_length=30)
    fName = models.CharField(max_length=30)
    last4Digits = models.CharField(max_length=15)
    # form can be empty; database can be null
    gender = models.CharField(max_length=10, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    address = models.CharField(max_length=256, blank=True, null=True)
    email = models.CharField(max_length=256, blank=True, null=True)
    accountInfo = models.CharField(max_length=256, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.fName = self.fName.lower()
        self.lName = self.lName.lower()
        self.studentID = self.studentID.lower()
        self.last4Digits = self.last4Digits.lower()
        self.gender = self.gender.lower()
        
        if self.gender:
            self.gender = self.gender.lower()
        if self.address:
            self.address = self.address.lower()
        if self.email:
            self.email = self.email.lower()
        if self.note:
            self.note = self.note.lower()
        
        return super(Student, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.lName + ', ' + self.fName