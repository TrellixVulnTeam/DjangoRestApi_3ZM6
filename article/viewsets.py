from django.core.serializers import get_serializer
from django.db.models import Count
from django.views.generic import detail
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework_extensions.mixins import NestedViewSetMixin

import article
from core.viewsets import BaseModelViewSet

from .models import Post, Comments, Like
from .serializers import PostSerializer, CommentsSerializer


class PostViewSet(BaseModelViewSet):
    queryset = Post.objects.all().annotate(like_count=Count("likes"), comment_count=Count("comments"))
    serializer_class = PostSerializer

    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ["title", "author__first_name", "author__last_name"]
    ordering = ["created"]
    ordering_fields = ["title", "author__username"]
    filterset_fields = ["title", "created", "author__username", "body"]

    @action(methods=["post"], detail=True, url_path="likes", url_name="like", permission_classes=[AllowAny])
    def like(self, request, *args, **kwargs):
        post = self.get_object()
        session_key = request.data.get("session_key", request.session.session_key or request.META.get('REMOTE_ADDR'))

        if session_key is not None:
            if liked_post := post.likes.filter(session_key=session_key).first():
                liked_post.delete()
            else:
                article.models.Like.objects.create(session_key=session_key, post=post)
        return Response({"likes": post.likes.count()})

    @action(methods=["get"], detail=True, url_path="toplike", url_name="toplike", permission_classes=[AllowAny])
    def top_like(self, request, *args, **kwargs,):
        top = request.GET.get("top", "")
        if not top:
            top = 10
        qs = Post.objects.all().annotate(like_count=Count("likes")).order_by("-likes")[:int(top)]
        qs_serializer = self.get_serializer(qs, many=True)
        return Response(qs_serializer.data)

    @action(methods=["get"], detail=True, url_path="topbycomments", url_name="/api/article/posts/", permission_classes=[AllowAny])
    def top_by_comments(self, request, *args, **kwargs):
        top = request.GET.get("top", "")
        if not top:
            top = 10
        qs = Post.objects.all().annotate(comment_count=Count("comments"), like_count=Count("likes")).order_by("-comments").distinct()[:int(top)]
        qs_serializer = self.get_serializer(qs, many=True)
        return Response(qs_serializer.data)


class CommentViewSet(NestedViewSetMixin, BaseModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = [AllowAny]

    def get_serializer(self, *args, **kwargs):
        if kwargs.get("data"):
            kwargs("data").update(self.get_parents_query_dict())
        return super(CommentViewSet, self).get_serializer(*args, **kwargs)
