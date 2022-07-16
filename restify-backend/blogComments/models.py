from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from blogs.models import Blog
from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.signals import notify


class BlogComment(models.Model):
    blog = models.ForeignKey(to=Blog, on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=False)
    comment = models.CharField(max_length=600)


class BlogCommentLike(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=False)
    comment_liked = models.ForeignKey(to=BlogComment, on_delete=models.CASCADE, null=False)


@receiver(post_save, sender=BlogComment)
def handle_blog_comment_notification(sender, instance, created, **kwargs):
    blog = instance.blog
    user = blog.restaurant.user
    if created:
        notify.send(actor=sender, sender=instance, recipient=user,  verb='You received a comment on your blog')
