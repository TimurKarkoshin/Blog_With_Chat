from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    """Профиль пользователя"""

    class Meta:
        ordering = ["pk"]
        verbose_name = _("профиль")
        verbose_name_plural = _("профили")

    user: User = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

