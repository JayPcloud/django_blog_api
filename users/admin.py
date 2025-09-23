from django.contrib import admin

from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    
    readonly_fields = ['id', 'user',]
 
admin.site.register(Profile, ProfileAdmin)
