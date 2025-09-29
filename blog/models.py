from django.db import models
from django.utils.deconstruct import deconstructible
import os
from users.models import User
from cloudinary_storage.storage import MediaCloudinaryStorage


# @deconstructible
# class GenerateProfileImagePath():
    
#     def __init__(self):
#         pass

#     def __call__(self, instance, filename):
#         ext = filename.split('.')[-1]
#         path = f'media/blog/{instance.blog_post.pk}/media_files/'
#         name = f'post.{ext}'
#         return os.path.join(path, name)
    
# blog_post_media_path = GenerateProfileImagePath()



class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class BlogPost(models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name='blog_posts', blank=True, )

    def __str__(self, *args, **kwargs):
        return f"{self.author.username}:{self.content[:30]}" 


class BlogMedia(models.Model):
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='media')
    file = models.FileField(
        storage=MediaCloudinaryStorage(),
        upload_to='django/blog_api', null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self, *args, **kwargs):
        return f'{self.pk}' 
    

class Comment(models.Model):
    body = models.TextField()
    blog = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True,)
    author = models.ForeignKey(User, on_delete=models.CASCADE, )
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')



    def __str__(self, *args, **kwargs):
        return f'Comment on {self.blog.title}-{self.pk}'


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'liked_posts')
    blog = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='likes')


    class Meta:
        unique_together = ('user', 'blog')

    def __str__(self):
        return f"{self.user} liked {self.blog}"
    
    
    
class BookMark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'bookmarks')
    blog = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='bookmarks')


    class Meta:
        unique_together = ('user', 'blog')

    def __str__(self):
        return f"{self.user}_bookmarked_blog_{self.blog}"
    
    
# models.py
class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    actor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications_sent',)
    blog = models.ForeignKey(BlogPost, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
    verb = models.CharField(max_length=255)  # 'liked', 'commented'
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ('recipient', 'actor', 'blog', 'comment', 'verb')


    