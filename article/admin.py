from django.contrib import admin
from django.db.models import Count

from article.models import Post, Comments, Like


# Register your models here.

# admin.site.register(Post)
class CommentAdminModelInLine(admin.TabularInline):
    model = Comments
    extra = 1


class LikeAdminModelInLine(admin.TabularInline):
    model = Like
    extra = 0

    # def has_change_permission(self, request, obj) -> bool:
    #    return False

    # def has_add_permission(self, request, obj) -> bool:
    #    return False


@admin.register(Post)
class PostAdminModel(admin.ModelAdmin):
    inlines = [CommentAdminModelInLine, LikeAdminModelInLine]
    list_display = ("title", "slug", "created", "user_name", "like_count",)
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-created',)
    list_filter = ('status', 'created')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related("comments")

    def user_name(self, obj):
        return obj.author.username

    def count_like(self, obj):
        return Post.objects.values('id').annotate(likes_count=Count('likes'))

    def like_count(self, obj):
        return obj.like_count

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return (
            qs.prefetch_related("comments").select_related("author").annotate(like_count=Count('likes'))
        )


@admin.register(Comments)
class CommentsAdminModel(admin.ModelAdmin):
    list_display = ('post', 'author', 'created',)
    ordering = ('-created',)
    list_filter = ('author', 'created')
