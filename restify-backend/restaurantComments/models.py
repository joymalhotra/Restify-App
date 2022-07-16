from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from restaurants.models import Restaurant
from django.db.models.signals import post_save
from notifications.signals import notify
from django.dispatch import receiver


class RestaurantComment(models.Model):
    restaurant = models.ForeignKey(to=Restaurant, on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=False)
    comment = models.CharField(max_length=600)


class RestaurantCommentLike(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=False)
    comment_liked = models.ForeignKey(to=RestaurantComment, on_delete=models.CASCADE, null=False)


@receiver(post_save, sender=RestaurantComment)
def handle_restaurant_comment_notification(sender, instance, created, **kwargs):
    restaurant = instance.restaurant
    user = restaurant.user
    if created:
        notify.send(actor=sender, sender=instance, recipient=user,  verb='You received a comment on your blog')