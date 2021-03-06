from django.urls import path, include

from django.urls import path
from .views import PostListView, PostDetailView


urlpatterns = [
    path("", PostListView.as_view()),
    path('<slug:slug>/', PostDetailView.as_view(), name='post_detail')
]

