from dataclasses import field, fields
from doctest import debug_script
from email.mime import image
from pydoc import describe
from urllib import request
from wsgiref import validate
from rest_framework import serializers
from .models import Restaurant, RestaurantFollower, RestaurantImage, RestaurantLike, RestaurantMenuItem
from django.core.validators import URLValidator
from django.core.exceptions import ObjectDoesNotExist, ValidationError
import re


class RestaurantSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'address', 'postal_code', 'website', 'phone_number', 'description', 'logo']


class CreateRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['name', 'address', 'postal_code', 'website', 'phone_number', 'description', 'logo']
    
    def validate(self, attrs):

        try:
            Restaurant.objects.get(user=self.context['request'].user)
            raise serializers.ValidationError({"detail": "User can only create at most one restaurant"})
        except ObjectDoesNotExist:
            pass

        if attrs.get('phone_number', False):
            r = re.compile(r'\+1\d\d\d\d\d\d\d\d\d\d')
            if not r.match(attrs['phone_number']):
                raise serializers.ValidationError({"phone_number": "Please enter a valid 10 digit phone number (eg. +19051233211)"})

        if attrs.get('postal_code', False):
            r = re.compile(r'[A-Z]\d[A-Z]\d[A-Z]\d')
            if not r.match(attrs['postal_code']):
                raise serializers.ValidationError({"postal_code": "Please enter a valid 6 character postal code (eg. M5J2R8)"})

        # validate_url = URLValidator()
        # try:
        #     validate_url(attrs['website'])
        # except ValidationError:
        #     raise serializers.ValidationError({"website": "Please enter a valid URL (eg. www.google.com)"})

        return attrs

    def create(self, validated_data):
        
        restaurant = Restaurant.objects.create(
            user=self.context['request'].user,
            name=validated_data['name'],
            address=validated_data['address'],
            postal_code=validated_data['postal_code'],
            website=validated_data['website'],
            phone_number=validated_data['phone_number'],
            description=validated_data['description'],
            logo=validated_data['logo'],
        )

        restaurant.save()
        return restaurant


class EditRestaurantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Restaurant
        fields = ['name', 'address', 'postal_code', 'website', 'phone_number', 'description', 'logo']
    
    def validate(self, attrs):

        try:
            restaurant = Restaurant.objects.get(user=self.context['request'].user)
        except ObjectDoesNotExist:
            raise serializers.ValidationError({"detail": "Please create a restaurant"})

        if attrs.get('phone_number', False):
            r = re.compile(r'\+1\d\d\d\d\d\d\d\d\d\d')
            if not r.match(attrs['phone_number']):
                raise serializers.ValidationError({"phone_number": "Please enter a valid 10 digit phone number (eg. +19051233211)"})

        if attrs.get('postal_code', False):
            r = re.compile(r'[A-Z]\d[A-Z]\d[A-Z]\d')
            if not r.match(attrs['postal_code']):
                raise serializers.ValidationError({"postal_code": "Please enter a valid 6 character postal code (eg. M5J2R8)"})

        return attrs

    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.address = validated_data['address']
        instance.postal_code = validated_data['postal_code']
        instance.website = validated_data['website']
        instance.phone_number = validated_data['phone_number']
        instance.description = validated_data['description']
        instance.logo = validated_data['logo']

        instance.save()
        return instance


class ImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = RestaurantImage
        fields = ['image']

class AddImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = RestaurantImage
        fields = ['image']
    
    def validate(self, attrs):
        try:
            Restaurant.objects.get(user=self.context['request'].user)
        except ObjectDoesNotExist:
            raise serializers.ValidationError({"detail": "Please create a restaurant before creating a menu item"})
        
        return attrs
    
    def create(self, validated_data):

        restaurant_image = RestaurantImage.objects.create(
            restaurant=Restaurant.objects.get(user=self.context['request'].user),
            image=validated_data['image']
        )
        
        restaurant_image.save()
        return restaurant_image


class AddMenuItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = RestaurantMenuItem
        fields = ['name', 'price', 'description']
    
    def validate(self, attrs):
        try:
            Restaurant.objects.get(user=self.context['request'].user)
        except ObjectDoesNotExist:
            raise serializers.ValidationError({"detail": "Please create a restaurant before creating a menu item"})

        return attrs

    def create(self, validated_data):

        menu_item = RestaurantMenuItem.objects.create(
            restaurant=Restaurant.objects.get(user=self.context['request'].user),
            name=validated_data['name'],
            price=validated_data['price'],
            description=validated_data['description']
        )

        return menu_item


class MenuSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = RestaurantMenuItem
        fields = ['id', 'name', 'price', 'description']


class EditMenuItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = RestaurantMenuItem
        fields = ['name', 'price', 'description']
    
    def validate(self, attrs):
        try:
            Restaurant.objects.get(user=self.context['request'].user)
        except ObjectDoesNotExist:
            raise serializers.ValidationError({"detail": "Please create a restaurant before editing a menu item"})


        return attrs

    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.price = validated_data['price']
        instance.description = validated_data['description']

        instance.save()
        return instance

class RestaurantFollowSerializer(serializers.ModelSerializer):
    user = serializers.CharField(required=False)

    class Meta:
        model = RestaurantFollower
        fields = ['id', 'restaurant', 'user']

    def create(self, validated_data):
        if RestaurantFollower.objects.filter(user=self.context['request'].user,
                                             restaurant=validated_data['restaurant']).count() > 0:
            return RestaurantFollower.objects.get(user=self.context['request'].user,
                                                  restaurant=validated_data['restaurant'])

        restaurant_follower = RestaurantFollower.objects.create(
            user=self.context['request'].user,
            restaurant=validated_data['restaurant'],
        )

        return restaurant_follower


class RestaurantLikeSerializer(serializers.ModelSerializer):
    user = serializers.CharField(required=False)

    class Meta:
        model = RestaurantLike
        fields = ('id', 'user', 'restaurant')

    def create(self, validated_data):
        if RestaurantLike.objects.filter(user=self.context['request'].user, restaurant=validated_data['restaurant']).count() > 0:
            return RestaurantLike.objects.get(user=self.context['request'].user, restaurant=validated_data['restaurant'])

        restaurant_liked = RestaurantLike.objects.create(
            user=self.context['request'].user,
            restaurant=validated_data['restaurant'],
        )
        return restaurant_liked



class RestaurantRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = RestaurantImage
        fields = ['image']