from django.contrib.auth import get_user_model
from rest_framework import serializers

from core.serializers import BaseModelSerializer
from .models import Post, Comments

User = get_user_model()


class CommentsSerializer(BaseModelSerializer):
    class Meta:
        model = Comments
        fields = ("id", "author", "body",)


class PostSerializer(BaseModelSerializer):
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source="author"
    )
    like_count = serializers.IntegerField()
    #comment_count = serializers.IntegerField()
    comments = CommentsSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ("id", "author_id", "slug", "title", "body", "comments", "like_count",)
