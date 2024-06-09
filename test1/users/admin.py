from django.contrib import admin
from .models import User

# Register your models here.


class Adminmodel(admin.ModelAdmin):
    list_display=['name','email','password']


admin.site.register(User,Adminmodel)