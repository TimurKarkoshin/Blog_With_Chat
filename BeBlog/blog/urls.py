from django.urls import path
from .views import PostView, PostDetailView, RandomPost, AboutView

urlpatterns = [
    path("", PostView.as_view(), name="post-list"),
    path("post--<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("random/", RandomPost.as_view(), name="random"),
    path("about/", AboutView.as_view(), name="about"),
]
