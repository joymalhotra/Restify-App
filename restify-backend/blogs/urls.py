from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from blogs.views import CreateBlogAPIView, RestaurantBlogsAPIView, DeleteBlogAPIView, BlogAPIView, CreateBlogLikeAPIView, \
    DeleteBlogLikeAPIView, BlogLikeCountView, AllBlogLikesAPIView, FeedAPIView, BlogLikedAPIView

app_name = 'blogs'
urlpatterns = [
    path('create/', CreateBlogAPIView.as_view(), name='create-blog'),
    path('<int:blog_id>/delete/', DeleteBlogAPIView.as_view(), name='delete-blog'),
    path('<int:blog_id>/details/', BlogAPIView.as_view(), name='blog-details'),
    path('<int:restaurant_id>/all/', RestaurantBlogsAPIView.as_view(), name='all-blogs'),
    # path('edit/', CreateBlogAPIView.as_view(), name='create blog'),
    
    path('like/', CreateBlogLikeAPIView.as_view(), name='like blog'),
    path('<int:blog_id>/unlike/', DeleteBlogLikeAPIView.as_view(), name='unlike blog'),
    path('<int:blog_id>/likes/amount/', BlogLikeCountView.as_view(), name='number blog likes'),
    path('<int:blog_id>/likes/all/', AllBlogLikesAPIView.as_view(), name='all blog likes'),
    path('<int:blog_id>/liked/', BlogLikedAPIView.as_view(), name='liked blog'),



    path('feed/', FeedAPIView.as_view(), name='feed'),
]
