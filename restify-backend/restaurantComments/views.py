from django.shortcuts import render
from rest_framework.generics import get_object_or_404, RetrieveAPIView, UpdateAPIView, CreateAPIView, \
    DestroyAPIView, ListAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import RestaurantCommentSerializer, RestaurantCommentLikeSerializer
from restaurants.models import Restaurant
from .models import RestaurantComment, RestaurantCommentLike
from restaurants.models import Restaurant
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, PermissionDenied
# Create your views here.


class RestaurantCommentAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RestaurantCommentSerializer

    def get_object(self):
        return get_object_or_404(RestaurantComment, id=self.kwargs['restaurant_comment_id'])


class RestaurantCommentCreateAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RestaurantCommentSerializer


class RestaurantCommentDeleteAPIView(DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RestaurantCommentSerializer

    def get_object(self):

        if RestaurantComment.objects.filter(id=self.kwargs['restaurant_comment_id']).count() <= 0:
            raise Http404

        restaurant_comment = RestaurantComment.objects.get(id=self.kwargs['restaurant_comment_id'])

        if restaurant_comment.user != self.request.user:
            raise PermissionDenied

        return restaurant_comment


class RestaurantCommentLikeCreateAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RestaurantCommentLikeSerializer


class RestaurantCommentLikeDeleteAPIView(DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RestaurantCommentSerializer

    def get_object(self):
        if RestaurantComment.objects.filter(id=self.kwargs['restaurant_comment_id']).count() <= 0:
            raise Http404

        restaurant_comment = RestaurantComment.objects.get(id=self.kwargs['restaurant_comment_id'])
        if RestaurantCommentLike.objects.filter(user=self.request.user, comment_liked=restaurant_comment).count() <= 0:
            print('hello')
            raise PermissionDenied

        return RestaurantCommentLike.objects.get(user=self.request.user, comment_liked=restaurant_comment)


class RestaurantCommentLikeCountView(APIView):
    """
    A view that returns the count of active users.
    """
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer, )

    def get(self, request, *args, **kwargs):

        if RestaurantComment.objects.filter(id=self.kwargs['restaurant_comment_id']).count() <= 0:
            raise Http404

        restaurant_comment = RestaurantComment.objects.get(id=self.kwargs['restaurant_comment_id'])
        like_count = RestaurantCommentLike.objects.filter(comment_liked=restaurant_comment).count()
        content = {'comment_like_count': like_count}
        return Response(content, status=200)


class AllRestaurantCommentLikesAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RestaurantCommentLikeSerializer

    def get_queryset(self):
        if RestaurantComment.objects.filter(id=self.kwargs['restaurant_comment_id']).count() <= 0:
            raise Http404
        restaurant_comment = RestaurantComment.objects.get(id=self.kwargs['restaurant_comment_id'])
        return RestaurantCommentLike.objects.filter(comment_liked=restaurant_comment)


class AllRestaurantCommentAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RestaurantCommentSerializer

    def get_queryset(self):
        if Restaurant.objects.filter(id=self.kwargs['restaurant_id']).count() <= 0:
            raise Http404
        restaurant = Restaurant.objects.get(id=self.kwargs['restaurant_id'])
        return RestaurantComment.objects.filter(restaurant=restaurant)
