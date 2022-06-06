from django.contrib import admin
from .models import Post , BlogComment
# Register your models here.
admin.site.register((Post,BlogComment))



# Superuser detail
# name = admin
# password =1234