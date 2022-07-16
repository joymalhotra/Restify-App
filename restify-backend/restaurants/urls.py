from django.urls import path
from restaurants.views import AddImageAPIView, CreateRestaurantAPIView, DeleteImageAPIView, EditMenuItemAPIView, \
RestaurantAPIView, EditRestaurantAPIView, RestaurantFollowAPIView, RestaurantUnfollowAPIView, RestaurantLikeAPIView, \
RestaurantUnlikeAPIView, ImagesAPIView, AddMenuItemAPIView, DeleteMenuItemAPIView, MenuAPIView, RestaurantFollowedView, \
RestaurantLikedView, RestaurantNumberFollowersView, RestaurantNumberLikedView, RestaurantImagesView, RestaurantListView

app_name = 'restaurants'
urlpatterns = [
    path('create/', CreateRestaurantAPIView.as_view(), name='create-restaurant'),
    path('edit/', EditRestaurantAPIView.as_view(), name="edit-restaurant"),
    path('my-restaurant/', RestaurantAPIView.as_view(), name='my-restaurant'),
    path('<int:restaurant_id>/view/', RestaurantAPIView.as_view(), name='view-restaurant'),
    
    path('image/add/', AddImageAPIView.as_view(), name='add-image'),
    path('image/<int:image_id>/delete/', DeleteImageAPIView.as_view(), name='delete-image'),
    path('<int:restaurant_id>/image/all/', ImagesAPIView.as_view(), name='all-images'),

    path('menu/add/', AddMenuItemAPIView.as_view(), name="add-menu-item"),
    path('menu/<int:menu_item_id>/delete/', DeleteMenuItemAPIView.as_view(), name="delete-menu-item"),
    path('menu/<int:menu_item_id>/edit/', EditMenuItemAPIView.as_view(), name="edit-menu-item"),
    path('<restaurant_id>/menu/view/', MenuAPIView.as_view(), name="view-menu"),

    path('follow/', RestaurantFollowAPIView.as_view(), name="follow-restaurant"),
    path('<int:restaurant_id>/unfollow/', RestaurantUnfollowAPIView.as_view(), name="unfollow-restaurant"),

    path('like/', RestaurantLikeAPIView.as_view(), name="like-restaurant"),
    path('<int:restaurant_id>/unlike/', RestaurantUnlikeAPIView.as_view(), name="unlike-restaurant"),
    path('search/<str:q>/', RestaurantListView.as_view(), name="Restaurant-Serach"),
    path('followed/<int:restaurant_id>/', RestaurantFollowedView.as_view(), name="Restaurant-Followed"),
    path('liked/<int:restaurant_id>/', RestaurantLikedView.as_view(), name="Restaurant-Followed"),
    path('numberfollowers/<int:restaurant_id>/', RestaurantNumberFollowersView.as_view(), name="Number-followers"),
    path('numberlikes/<int:restaurant_id>/', RestaurantNumberLikedView.as_view(), name="Number-likes"),
    path('images/<int:restaurant_id>/', RestaurantImagesView.as_view(), name="Images-Retrieval"), 

]
