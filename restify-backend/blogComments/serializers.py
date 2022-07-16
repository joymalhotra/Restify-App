from rest_framework import serializers
from django.contrib.auth.models import User
from .models import BlogComment, BlogCommentLike
from blogs.models import Blog


class BlogCommentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(required=False)

    class Meta:
        model = BlogComment
        fields = ['id', 'blog', 'user',  'comment']

    def create(self, validated_data):
        blog_comment = BlogComment.objects.create(
            user=self.context['request'].user,
            blog=validated_data['blog'],
            comment=validated_data['comment']

        )
        return blog_comment


class BlogCommentLikeSerializer(serializers.ModelSerializer):
    user = serializers.CharField(required=False)

    class Meta:
        model = BlogCommentLike
        fields = ('id', 'user', 'comment_liked')

    def create(self, validated_data):
        if BlogCommentLike.objects.filter(user=self.context['request'].user,
                                          comment_liked=validated_data['comment_liked']).count() > 0:
            return BlogCommentLike.objects.get(user=self.context['request'].user,
                                               comment_liked=validated_data['blog_liked'])

        blog_comment_like = BlogCommentLike.objects.create(
            user=self.context['request'].user,
            comment_liked=validated_data['comment_liked'],
        )

        return blog_comment_like
