from django.contrib import admin
from .models import BlogPost, BlogMedia, Comment, Like, Tag, Notification

# Register your models here.

class BlogPostAdmin(admin.ModelAdmin):
    
    readonly_fields = ['id', 'author', 'created_at', 'updated_at']
 
admin.site.register(BlogPost, BlogPostAdmin)


class BlogMediaAdmin(admin.ModelAdmin):
    
    readonly_fields = ['id', 'created_at',]
 
admin.site.register(BlogMedia, BlogMediaAdmin)


class BlogCommentAdmin(admin.ModelAdmin):
    
    readonly_fields = ['id', 'created_at',]
 
admin.site.register(Comment, BlogCommentAdmin)


class BlogLikeAdmin(admin.ModelAdmin):
    
    readonly_fields = ['id',]
 
admin.site.register(Like, BlogLikeAdmin)


class BlogTagAdmin(admin.ModelAdmin):
    
    readonly_fields = ['id']
 
admin.site.register(Tag, BlogTagAdmin)



class NotificationAdmin(admin.ModelAdmin):
    
    readonly_fields = ['id', 'actor', 'recipient',]
 
admin.site.register(Notification, NotificationAdmin)


