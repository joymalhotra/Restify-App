from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from blogComments.views import BlogCommentAPIView, BlogCommentCreateAPIView, BlogCommentLikeCreateAPIView, \
    BlogCommentDeleteAPIView, BlogCommentLikeCountView, AllBlogCommentLikesAPIView, BlogCommentLikeDeleteAPIView, AllBlogCommentsAPIView

app_name = 'blogComments'

urlpatterns = [
    path('create/', BlogCommentCreateAPIView.as_view(), name='create-blogComment'),
    path('<int:blog_comment_id>/delete/', BlogCommentDeleteAPIView.as_view(), name='delete-blogComment'),
    path('<int:blog_comment_id>/details/', BlogCommentAPIView.as_view(), name='blogComment-details'),
    path('<int:blog_id>/all/', AllBlogCommentsAPIView.as_view(), name='all-blogComments'),

    path('like/', BlogCommentLikeCreateAPIView.as_view(), name='create-blogComment'),
    path('<int:blog_comment_id>/unlike/', BlogCommentLikeDeleteAPIView.as_view(), name='delete-blogCommentLike'),

    path('<int:blog_comment_id>/likes/all/', AllBlogCommentLikesAPIView.as_view(), name='all-blogCommentLike'),
    path('<int:blog_comment_id>/likes/amount/', BlogCommentLikeCountView.as_view(), name='blogCommentLikes-count'),


]
