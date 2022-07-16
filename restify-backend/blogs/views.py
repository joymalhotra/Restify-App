from django.shortcuts import render
from rest_framework.generics import get_object_or_404, RetrieveAPIView, UpdateAPIView, CreateAPIView, \
    DestroyAPIView, ListAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import BlogSerializer, CreateBlogSerializer, BlogLikeSerializer
from restaurants.models import Restaurant, RestaurantFollower
from .models import Blog, BlogLike
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.db.models import Q

from django.http import FileResponse

# Create your views here.


class FeedAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BlogSerializer

    def get_queryset(self):
        if RestaurantFollower.objects.filter(user=self.request.user).count() <= 0:
            return {}

        all_restaurant = RestaurantFollower.objects.filter(user=self.request.user).values('restaurant')
        return Blog.objects.filter(restaurant__in=all_restaurant).order_by('-created_at')


class RestaurantBlogsAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BlogSerializer

    def get_queryset(self):
        if Restaurant.objects.filter(id=self.kwargs['restaurant_id']).count() <= 0:
            return {}
        restaurant = Restaurant.objects.get(id=self.kwargs['restaurant_id'])
        return Blog.objects.filter(restaurant=restaurant)


class BlogAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BlogSerializer

    def get_object(self):
        return get_object_or_404(Blog, id=self.kwargs['blog_id'])


class CreateBlogAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CreateBlogSerializer


class DeleteBlogAPIView(DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BlogSerializer

    def get_object(self):
        if Blog.objects.filter(id=self.kwargs['blog_id']).count() <= 0:
            raise Http404
        if Restaurant.objects.filter(user=self.request.user).count() <= 0:
            raise PermissionDenied

        restaurant = Restaurant.objects.get(user=self.request.user)
        if Blog.objects.filter(restaurant=restaurant, id=self.kwargs['blog_id']).count() <= 0:
            raise PermissionDenied

        return Blog.objects.get(restaurant=restaurant, id=self.kwargs['blog_id'])


class CreateBlogLikeAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BlogLikeSerializer


class DeleteBlogLikeAPIView(DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BlogLikeSerializer

    def get_object(self):
        if Blog.objects.filter(id=self.kwargs['blog_id']).count() <= 0:
            raise Http404

        blog = Blog.objects.get(id=self.kwargs['blog_id'])

        if BlogLike.objects.filter(blog_liked=blog, user=self.request.user).count() <= 0:
            raise PermissionDenied

        return BlogLike.objects.get(blog_liked=blog, user=self.request.user)


class BlogLikeCountView(APIView):
    """
    A view that returns the count of active users.
    """
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer, )

    def get(self, request, *args, **kwargs):

        if Blog.objects.filter(id=self.kwargs['blog_id']).count() <= 0:
            raise Http404

        blog = Blog.objects.get(id=self.kwargs['blog_id'])
        like_count = BlogLike.objects.filter(blog_liked=blog).count()
        content = {'like_count': like_count}
        return Response(content, status=200)


class AllBlogLikesAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BlogLikeSerializer

    def get_queryset(self):
        if Blog.objects.filter(id=self.kwargs['blog_id']).count() <= 0:
            raise Http404
        blog = Blog.objects.get(id=self.kwargs['blog_id'])
        return BlogLike.objects.filter(blog_liked=blog)


class BlogLikedAPIView(APIView):

    permission_classes = [IsAuthenticated]
    http_method_names = ['get']
    # serializer_class = RestaurantFollowedSerializer

    def get(self, request, *args, **kwargs):
        query = self.kwargs['blog_id']

        q = Blog.objects.filter(id=query)
        if not q.exists():
            raise Http404

        if query:
            q1 = BlogLike.objects.filter(Q(user=self.request.user) & Q(blog_liked=query))
        
        if q1.exists():
            content = {'liked': 'True'}
            return Response(content, 200)
            
        else:
            content = {'liked': 'False'}
            return Response(content, 200)