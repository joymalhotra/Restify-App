from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from restaurantComments.views import RestaurantCommentAPIView, RestaurantCommentCreateAPIView, \
    RestaurantCommentLikeCreateAPIView, RestaurantCommentDeleteAPIView, RestaurantCommentLikeCountView, \
    AllRestaurantCommentLikesAPIView, RestaurantCommentLikeDeleteAPIView, AllRestaurantCommentAPIView

app_name = 'restaurantComments'

urlpatterns = [
    path('create/', RestaurantCommentCreateAPIView.as_view(), name='create-restaurantComment'),
    path('<int:restaurant_comment_id>/delete/', RestaurantCommentDeleteAPIView.as_view(), name='delete-restaurantComment'),
    path('<int:restaurant_comment_id>/details/', RestaurantCommentAPIView.as_view(), name='restaurantComment-details'),
    path('<int:restaurant_id>/all/', AllRestaurantCommentAPIView.as_view(), name='all-restaurantComments'),

    path('like/', RestaurantCommentLikeCreateAPIView.as_view(), name='create-restaurantCommentLike'),
    path('<int:restaurant_comment_id>/unlike/', RestaurantCommentLikeDeleteAPIView.as_view(), name='delete-restaurantCommentLike'),

    path('<int:restaurant_comment_id>/likes/all/', AllRestaurantCommentLikesAPIView.as_view(), name='all-restaurantCommentLike'),
    path('<int:restaurant_comment_id>/likes/amount/', RestaurantCommentLikeCountView.as_view(), name='restaurantCommentLikes-count'),

]