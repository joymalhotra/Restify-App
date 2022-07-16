from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404, RetrieveAPIView, UpdateAPIView, CreateAPIView, DestroyAPIView, ListAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from restaurants.models import Restaurant, RestaurantFollower, RestaurantImage, RestaurantLike, RestaurantMenuItem
from .serializers import AddImageSerializer, AddMenuItemSerializer, CreateRestaurantSerializer, EditRestaurantSerializer, MenuSerializer, \
RestaurantSerializer, RestaurantFollowSerializer, RestaurantLikeSerializer, EditMenuItemSerializer, ImageSerializer, RestaurantRetrieveSerializer
from django.http import Http404
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
import django_filters
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from itertools import chain
# Create your views here.


class CreateRestaurantAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateRestaurantSerializer


class RestaurantAPIView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RestaurantSerializer

    def get_object(self):
        if ('restaurant_id' in self.kwargs):
            return get_object_or_404(Restaurant, id=self.kwargs['restaurant_id']) 
        
        return get_object_or_404(Restaurant, user=self.request.user) 
    

class EditRestaurantAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EditRestaurantSerializer

    def get_object(self):
        return get_object_or_404(Restaurant, user=self.request.user)


class ImagesAPIView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ImageSerializer

    def get_queryset(self):
        try:
            restaurant = Restaurant.objects.get(id=self.kwargs['restaurant_id'])
        except ObjectDoesNotExist:
            raise Http404
        restaurant_images = RestaurantImage.objects.filter(restaurant=restaurant)

        return restaurant_images


class AddImageAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddImageSerializer


class DeleteImageAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ImageSerializer

    def get_object(self):
        try:
            image = RestaurantImage.objects.get(id=self.kwargs['image_id'])
        except ObjectDoesNotExist:
            raise Http404

        return image

class AddMenuItemAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddMenuItemSerializer


class DeleteMenuItemAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MenuSerializer

    def get_object(self):
        try:
            menu_item = RestaurantMenuItem.objects.get(id=self.kwargs['menu_item_id'])
        except ObjectDoesNotExist:
            raise Http404

        return menu_item


class EditMenuItemAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EditMenuItemSerializer

    def get_object(self):
        return get_object_or_404(RestaurantMenuItem, id=self.kwargs['menu_item_id'])


class MenuAPIView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = MenuSerializer

    def get_queryset(self):
        try:
            restaurant = Restaurant.objects.get(id=self.kwargs['restaurant_id'])
        except ObjectDoesNotExist:
            raise Http404
        menu_items = RestaurantMenuItem.objects.filter(restaurant=restaurant)

        return menu_items


class RestaurantFollowAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RestaurantFollowSerializer


class RestaurantUnfollowAPIView(DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RestaurantFollowSerializer

    def get_object(self):
        if Restaurant.objects.filter(id=self.kwargs['restaurant_id']).count() <= 0:
            raise Http404

        restaurant = Restaurant.objects.get(id=self.kwargs['restaurant_id'])
        if RestaurantFollower.objects.filter(user=self.request.user, restaurant=restaurant).count() <= 0:
            raise PermissionDenied

        return RestaurantFollower.objects.get(user=self.request.user, restaurant=restaurant)


class RestaurantLikeAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RestaurantLikeSerializer


class RestaurantUnlikeAPIView(DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RestaurantLikeSerializer

    def get_object(self):
        if Restaurant.objects.filter(id=self.kwargs['restaurant_id']).count() <= 0:
            raise Http404

        restaurant = Restaurant.objects.get(id=self.kwargs['restaurant_id'])

        if RestaurantLike.objects.filter(restaurant=restaurant, user=self.request.user).count() <= 0:
            raise PermissionDenied

        return RestaurantLike.objects.get(restaurant=restaurant, user=self.request.user)


class RestaurantListView(APIView):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        query = self.kwargs['q']
        if query:
            res1 = RestaurantMenuItem.objects.filter(Q(name=query)).values_list('restaurant__name','restaurant__id').distinct()
            res2 = Restaurant.objects.filter(Q(name=query) | Q(address=query)).values_list('name', 'id')
            union = list(chain(res1, res2))
            return Response(union)
        

# restaurant followed 
class RestaurantFollowedView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        query = self.kwargs['restaurant_id']

        q = Restaurant.objects.filter(id=query)
        if not q.exists():
            raise Http404
                 
        if query:
            q1 = RestaurantFollower.objects.filter(Q(user=self.request.user) & Q(restaurant=query))

        if q1.exists():
            content = {'Restaurant Followed': 'True'}
            return Response(content, 200)
            
        else:
            content = {'Restaurant Followed': 'False'}
            return Response(content, 200)

        
class RestaurantLikedView(APIView):

    permission_classes = [IsAuthenticated]
    http_method_names = ['get']
    # serializer_class = RestaurantFollowedSerializer

    def get(self, request, *args, **kwargs):
        query = self.kwargs['restaurant_id']

        q = Restaurant.objects.filter(id=query)
        if not q.exists():
            raise Http404

        if query:
            q1 = RestaurantLike.objects.filter(Q(user=self.request.user) & Q(restaurant=query))
        
        if q1.exists():
            content = {'Restaurant Liked': 'True'}
            return Response(content, 200)
            
        else:
            content = {'Restaurant Liked': 'False'}
            return Response(content, 200)

class RestaurantNumberFollowersView(APIView):
    permission_classes = (AllowAny,)
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        query = self.kwargs['restaurant_id']
       
        q = Restaurant.objects.filter(id=query)
        if not q.exists():
            raise Http404
        
        if query:
            num = RestaurantFollower.objects.filter(restaurant=query).count()
        
        content = {'Number Followers': num} 
        return Response(content, 200)

class RestaurantNumberLikedView(APIView):
    permission_classes = (AllowAny,)
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        query = self.kwargs['restaurant_id']

        q = Restaurant.objects.filter(id=query)
        if not q.exists():
            raise Http404

        if query:
            num = RestaurantLike.objects.filter(restaurant=query).count()
        
        content = {'Number Liked': num} 
        return Response(content, 200)


class RestaurantImagesView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RestaurantRetrieveSerializer
    

    def get_queryset(self):
        query = self.kwargs['restaurant_id']
        RestaurantRetrieveSerializer

        q = Restaurant.objects.filter(id=query)
        if not q.exists():
            raise Http404

        if query:
            return  RestaurantImage.objects.filter(restaurant=query)






















