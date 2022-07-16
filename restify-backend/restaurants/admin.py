from django.contrib import admin

# Register your models here.
from restaurants.models import Restaurant, RestaurantImage, RestaurantFollower, RestaurantLike, RestaurantMenuItem

admin.site.register(Restaurant)
admin.site.register(RestaurantFollower)
admin.site.register(RestaurantImage)
admin.site.register(RestaurantLike)
admin.site.register(RestaurantMenuItem)
