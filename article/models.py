from ckeditor.fields import RichTextField
from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()
status = (("draft", "Draft"), ("publish", "Publish"))


class PostQuerySet(models.query.QuerySet):

    def draft(self):
        return self.filter(status="draft")

    def publish(self):
        return self .filter(status="publish")


class PostManager(models.Manager):
    def get_query_set(self):
        return PostQuerySet(self.model)

    def draft(self):
        return self.get_query_set().draft()

    def publish(self):
        return self.get_query_set().publish()


class Post(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, unique=True)
    body = RichTextField()
    status = models.CharField(max_length=20, choices=status)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    update = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=100, unique=True)

    objects = PostManager()

    class Meta:
        default_related_name = "posts"
        ordering = ("created",)

    def __str__(self) -> str:
        return f"{self.pk}:{self.title}"


class Comments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.CharField(max_length=60)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("created",)


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    session_key = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (("post", "session_key"),)
