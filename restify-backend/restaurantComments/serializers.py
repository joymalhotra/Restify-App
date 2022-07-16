from rest_framework import serializers
from django.contrib.auth.models import User
from .models import RestaurantComment, RestaurantCommentLike
from restaurants.models import Restaurant


class RestaurantCommentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(required=False)

    class Meta:
        model = RestaurantComment
        fields = ['id', 'restaurant', 'user', 'comment']

    def create(self, validated_data):
        restaurant_comment = RestaurantComment.objects.create(
            user=self.context['request'].user,
            restaurant=validated_data['restaurant'],
            comment=validated_data['comment']

        )
        return restaurant_comment


class RestaurantCommentLikeSerializer(serializers.ModelSerializer):
    user = serializers.CharField(required=False)

    class Meta:
        model = RestaurantCommentLike
        fields = ('id', 'user', 'comment_liked')

    def create(self, validated_data):
        if RestaurantCommentLike.objects.filter(user=self.context['request'].user,
                                                comment_liked=validated_data['comment_liked']).count() > 0:
            return RestaurantCommentLike.objects.get(user=self.context['request'].user,
                                                     comment_liked=validated_data['comment_liked'])

        restaurant_comment_like = RestaurantCommentLike.objects.create(
            user=self.context['request'].user,
            comment_liked=validated_data['comment_liked'],
        )

        return restaurant_comment_like
