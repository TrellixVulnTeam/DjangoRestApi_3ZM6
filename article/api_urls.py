from rest_framework_extensions.routers import ExtendedDefaultRouter
from .viewsets import PostViewSet, CommentViewSet

router = ExtendedDefaultRouter()

posts_router = router.register(r"posts", PostViewSet, basename="posts")

posts_router.register(r"comments", CommentViewSet, basename="comments", parents_query_lookups=["post_id"])

urlpatterns = router.urls
