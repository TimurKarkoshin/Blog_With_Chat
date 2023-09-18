from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.base import RedirectView
from django.views import View
from .models import Post
from django.shortcuts import render
from random import choice


class PostView(ListView):
    """
    Предстиавление для отображения постов
    """
    model = Post


class PostDetailView(DetailView):
    """
    Детальное представление поста
    """
    model = Post
    context_object_name = "post"


class RandomPost(RedirectView):
    is_permanent = True

    def get_redirect_url(*args, **kwargs):
        return f"/BeBlog/post--{choice(Post.objects.filter().values_list('id', flat=True))}/"


class AboutView(View):
    template_name = "info/about.html"

    def get(self, request):
        return render(request, self.template_name)
