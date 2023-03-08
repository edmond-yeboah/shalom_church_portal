from django.db import models
from accounts.models import Customusers

# Create your models here.

class sermon(models.Model):
    title = models.CharField(blank=True, null=True, max_length=50)
    content = models.CharField(blank=True,null=True, max_length=5000)
    image = models.ImageField(upload_to='sermon_images')
    added_on = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    


class announcement(models.Model):
    title = models.CharField(blank=True, null=True, max_length=50)
    content = models.CharField(blank=True,null=True, max_length=5000)
    added_on = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(Customusers,on_delete=models.CASCADE)

    def __str__(self):
        return self.title