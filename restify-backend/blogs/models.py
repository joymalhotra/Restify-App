
# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from restaurants.models import Restaurant, RestaurantFollower
from django.db.models.signals import post_save
from notifications.signals import notify
from django.dispatch import receiver


class Blog(models.Model):
    restaurant = models.ForeignKey(to=Restaurant, on_delete=models.CASCADE, null=False)
    title = models.CharField(max_length=200)
    main_image = models.ImageField(upload_to='pictures')
    intro = models.TextField()

    heading1 = models.CharField(max_length=200)
    para1 = models.TextField()
    section_image1 = models.ImageField(null=True, blank=True, upload_to='pictures')

    heading2 = models.CharField(max_length=200, null=True)
    para2 = models.TextField(null=True)
    section_image2 = models.ImageField(null=True, blank=True, upload_to='pictures')

    conclusion = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class BlogLike(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=False)
    blog_liked = models.ForeignKey(to=Blog, on_delete=models.CASCADE, null=False)
    created_at = models.DateTimeField(auto_now_add=True)


@receiver(post_save, sender=Blog)
def handle_blog_notification(sender, instance, created, **kwargs):
    restaurant = instance.restaurant
    restaurant_followers = RestaurantFollower.objects.filter(restaurant=restaurant).values('user')
    users = User.objects.filter(id__in=restaurant_followers)

    if created:
        notify.send(actor=sender, sender=instance, recipient=users,  verb='a restaurant you follow has posted a blog')


@receiver(post_save, sender=BlogLike)
def handle_blog_like_notification(sender, instance, created, **kwargs):
    blog_liked = instance.blog_liked
    restaurant = blog_liked.restaurant
    if created:
        notify.send(actor=sender, sender=instance, recipient=restaurant.user,  verb='Someone liked your blog')