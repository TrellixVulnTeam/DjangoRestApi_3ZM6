from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.shortcuts import render
from .models import Post, Comments


# Create your views here.


# def hello_world(request):
#    return HttpResponse('<h1>Hello</h1>')

class PostListView(ListView):
    queryset = Post.objects.publish()
    template_name = 'article/index.html'


class PostDetailView(DetailView):
    model = Post
    template_name = 'article/post_detail.html'


