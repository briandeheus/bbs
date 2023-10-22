from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    display_name = models.CharField(max_length=1024)
    avatar_url = models.CharField(max_length=1024)
    profile_url = models.URLField()
    authorization_token = models.CharField(max_length=128)
    mastodon_registration_date = models.DateTimeField()
    mastodon_post_count = models.IntegerField(default=0)
