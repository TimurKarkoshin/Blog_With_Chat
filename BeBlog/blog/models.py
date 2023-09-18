from user.models import User
from django.db import models


class Post(models.Model):
    """Модель публикации"""

    title = models.CharField(max_length=512, verbose_name="пост")
    description = models.TextField(max_length=256, verbose_name="описание")
    content = models.TextField(verbose_name="контент")
    author = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(verbose_name="изображение", upload_to="blog/", blank=True)

    def __str__(self):
        return f"{self.title}, {self.author}"

    class Meta:
        verbose_name_plural = "посты"
        verbose_name = "пост"
