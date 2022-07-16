from django.contrib import admin

# Register your models here.
from restaurantComments.models import RestaurantComment, RestaurantCommentLike

admin.site.register(RestaurantComment)
admin.site.register(RestaurantCommentLike)
