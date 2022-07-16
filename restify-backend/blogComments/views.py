from django.shortcuts import render
from rest_framework.generics import get_object_or_404, RetrieveAPIView, UpdateAPIView, CreateAPIView, \
    DestroyAPIView, ListAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import BlogCommentSerializer, BlogCommentLikeSerializer
from restaurants.models import Restaurant
from .models import BlogComment, BlogCommentLike
from blogs.models import Blog
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, PermissionDenied
# Create your views here.


class BlogCommentAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BlogCommentSerializer

    def get_object(self):
        return get_object_or_404(BlogComment, id=self.kwargs['blog_comment_id'])


class BlogCommentCreateAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BlogCommentSerializer


class BlogCommentDeleteAPIView(DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BlogCommentSerializer

    def get_object(self):
        if BlogComment.objects.filter(id=self.kwargs['blog_comment_id']).count() <= 0:
            raise Http404

        blog_comment = BlogComment.objects.get(id=self.kwargs['blog_comment_id'])

        if blog_comment.user != self.request.user:
            raise PermissionDenied

        return blog_comment


class BlogCommentLikeCreateAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BlogCommentLikeSerializer


class BlogCommentLikeDeleteAPIView(DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BlogCommentSerializer

    def get_object(self):
        if BlogComment.objects.filter(id=self.kwargs['blog_comment_id']).count() <= 0:
            raise Http404

        blog_comment = BlogComment.objects.get(id=self.kwargs['blog_comment_id'])
        if BlogCommentLike.objects.filter(user=self.request.user, comment_liked=blog_comment).count() <= 0:
            raise PermissionDenied

        return BlogCommentLike.objects.get(user=self.request.user, comment_liked=blog_comment)


class BlogCommentLikeCountView(APIView):
    """
    A view that returns the count of active users.
    """
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer, )

    def get(self, request, *args, **kwargs):

        if BlogComment.objects.filter(id=self.kwargs['blog_comment_id']).count() <= 0:
            raise Http404

        blog_comment = BlogComment.objects.get(id=self.kwargs['blog_comment_id'])
        like_count = BlogCommentLike.objects.filter(comment_liked=blog_comment).count()
        content = {'comment_like_count': like_count}
        return Response(content, status=200)


class AllBlogCommentLikesAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BlogCommentLikeSerializer

    def get_queryset(self):
        if BlogCommentLike.objects.filter(id=self.kwargs['blog_comment_id']).count() <= 0:
            raise Http404
        blog_comment = BlogComment.objects.get(id=self.kwargs['blog_comment_id'])
        return BlogCommentLike.objects.filter(comment_liked=blog_comment)


class AllBlogCommentsAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BlogCommentSerializer

    def get_queryset(self):
        if Blog.objects.filter(id=self.kwargs['blog_id']).count() <= 0:
            raise Http404
        blog = Blog.objects.get(id=self.kwargs['blog_id'])
        return BlogComment.objects.filter(blog=blog)