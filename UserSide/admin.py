from django.contrib import admin
from .models import Payment, comment, family

# Register your models here.
admin.site.register(comment)
admin.site.register(Payment)
admin.site.register(family)