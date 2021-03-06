from django.urls import include, path

urlpatterns = [
    path("account/", include("account.urls")),
    path("article/", include("article.api_urls"))
]