# signals.py
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from .models import Like, Comment, Notification


@receiver(post_save, sender=Like)
def handle_like_notification(sender, instance, created, **kwargs):
    if created and instance.blog.author != instance.user:
        Notification.objects.get_or_create(
            recipient=instance.blog.author,
            actor=instance.user,
            blog=instance.blog,
            verb='liked',
        )


@receiver(post_delete, sender=Like)
def handle_unlike_notification(sender, instance, **kwargs):
    if instance.blog.author != instance.user:
        Notification.objects.filter(
            recipient=instance.blog.author,
            actor=instance.user,
            blog=instance.blog,
            verb='liked',
        ).update(is_active=False)


@receiver(post_save, sender=Comment)
def handle_comment_notification(sender, instance, created, **kwargs):
    if created and instance.blog.author != instance.author:
        Notification.objects.get_or_create(
            recipient=instance.blog.author,
            actor=instance.author,
            blog=instance.blog,
            comment=instance,
            verb='commented',
        )
        
@receiver(post_delete, sender=Comment)
def deactivate_comment_notification(sender, instance, **kwargs):
    if instance.blog.author != instance.author:
        Notification.objects.filter(
        recipient=instance.blog.author,
        actor=instance.author,
        blog=instance.blog,
        comment=instance,
        verb='commented',
        ).update(is_active=False)
        
