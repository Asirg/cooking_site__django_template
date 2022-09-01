from django.db import models
from django.contrib.auth import get_user_model

from nyamki.models import Article

class Profile(models.Model):
    user = models.OneToOneField(to=get_user_model(),on_delete=models.CASCADE)

    save_articles = models.ManyToManyField(
        to=Article, blank=True, verbose_name="Сохраненные статьи ", related_name="save_articles"
    )

    def __str__(self):
        return f"profile:{self.user}"

class UserAvatar(models.Model):
    profile = models.OneToOneField(to=Profile, on_delete=models.CASCADE)
    image = models.ImageField("Аватар", upload_to="user/avatar/", blank=True, null=True)