from django.db import models

class Program(models.Model):
    programName = models.CharField(max_length=250, unique=True)
    # curriculum number
    programCode = models.CharField(max_length=250, unique=True)
    length = models.IntegerField()
    cost = models.IntegerField()
    isActive = models.BooleanField(default=True)
    expiresAt = models.DateField(max_length=15, blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.programName = self.programName.lower()
        self.programCode = self.programCode.lower()
        if self.expiresAt == "":
            self.expiresAt = None
        return super(Program, self).save(*args, **kwargs)
    
    def __str__(self):
        return '%s' % self.programName