from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Customusers(AbstractUser):
    email = models.EmailField(null=True, blank=True, unique=True)
    tel = models.IntegerField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    admin = models.BooleanField(default=False)
    bio = models.CharField(max_length=1000, null=True, blank=True)
    church_branch = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=100,null=True,blank=True,default="Active")

    def __str__(self):
        return self.username


class quote(models.Model):
    title = models.CharField(max_length=50,null=True,blank=True)
    content = models.CharField(max_length=200,null=True,blank=True)
    verse = models.CharField(max_length=50,null=True,blank=True)

    def __str__(self):
        return self.title
    