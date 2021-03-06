import django_filters
from django.contrib.auth import get_user_model

from article.models import Post, Comments, Like

User = get_user_model()


class PostFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Post
        fields = ['author_id', 'title']


class CommentsFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Comments
        fields = ['id', 'author']


class UserFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = User
        fields = ['username', 'first_name']
