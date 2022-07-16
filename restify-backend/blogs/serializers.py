from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Blog, BlogLike
from restaurants.models import Restaurant
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class BlogSerializer(serializers.ModelSerializer):
    restaurant_id = serializers.IntegerField(source='restaurant.id')

    class Meta:
        model = Blog
        fields = ('id', 'restaurant_id', 'title', 'main_image', 'intro', 'heading1', 'para1', 'section_image1', 'heading2', 'para2',
                  'section_image2', 'conclusion', 'created_at', 'updated_at')


class CreateBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ('title', 'main_image', 'intro', 'heading1', 'para1', 'section_image1', 'heading2', 'para2',
                  'section_image2', 'conclusion')

    def validate(self, attrs):
        try:
            Restaurant.objects.get(user=self.context['request'].user)
        except ObjectDoesNotExist:
            raise serializers.ValidationError({"detail": "Please create a restaurant before creating a blog post"})

        return attrs

    def create(self, validated_data):
        print(validated_data)
        user = self.context['request'].user
        r = Restaurant.objects.get(user=user)

        blog = Blog.objects.create(
            restaurant=r,
            title=validated_data['title'],
            main_image=validated_data['main_image'],
            intro=validated_data['intro'],
            heading1=validated_data['heading1'],
            para1=validated_data['para1'],
            conclusion=validated_data['conclusion']
        )

        if validated_data.get('section_image1', False):
            blog.section_image1 = validated_data['section_image1']

        if validated_data.get('heading2', False):
            blog.heading2 = validated_data['heading2']

        if validated_data.get('para2', False):
            blog.para2 = validated_data['para2']

        if validated_data.get('section_image2', False):
            blog.section_image2 = validated_data['section_image2']

        blog.save()
        return blog


class BlogLikeSerializer(serializers.ModelSerializer):
    user = serializers.CharField(required=False)

    class Meta:
        model = BlogLike
        fields = ('id', 'user', 'blog_liked', 'created_at')

    def create(self, validated_data):
        if BlogLike.objects.filter(user=self.context['request'].user, blog_liked=validated_data['blog_liked']).count() > 0:
            return BlogLike.objects.get(user=self.context['request'].user, blog_liked=validated_data['blog_liked'])

        blog_like = BlogLike.objects.create(
            user=self.context['request'].user,
            blog_liked=validated_data['blog_liked'],

        )
        return blog_like


