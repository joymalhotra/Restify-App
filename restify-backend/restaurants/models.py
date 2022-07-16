from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models.signals import post_save
from notifications.signals import notify
from django.dispatch import receiver

class Restaurant(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=6)
    website = models.URLField()
    phone_number = PhoneNumberField()
    description = models.TextField()
    logo = models.ImageField()

    def __str__(self):
        return self.name

class RestaurantImage(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='images', on_delete=models.CASCADE, null=False)
    image = models.ImageField()

class RestaurantFollower(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

class RestaurantLike(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='menu_items', on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=200)
    price = models.FloatField()
    description = models.TextField()

    def __str__(self):
        return self.name

@receiver(post_save, sender=RestaurantFollower)
def handle_restaurant_follow_notification(sender, instance, created, **kwargs):
    restaurant = instance.restaurant
    if created:
        notify.send(actor=sender, sender=instance, recipient=restaurant.user,  verb='someone has followed you')


@receiver(post_save, sender=RestaurantLike)
def handle_restaurant_like_notification(sender, instance, created, **kwargs):
    restaurant_liked = instance.restaurant
    if created:
        notify.send(actor=sender, sender=instance, recipient=restaurant_liked.user,  verb='someone liked your restaurant')

@receiver(post_save, sender=RestaurantMenuItem)
def handle_restaurant_menu__update_notification(sender, instance, created, **kwargs):
    restaurant = instance.restaurant
    restaurant_followers = RestaurantFollower.objects.filter(restaurant=restaurant).values('user')
    users = User.objects.filter(id__in=restaurant_followers)

    if created:
        notify.send(actor=sender, sender=instance, recipient=users, verb='a restaurant you follow updated their menu')