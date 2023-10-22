from django.db import models


# Create your models here.
class Media(models.Model):
    actor = models.ForeignKey(
        "messageboard.User", on_delete=models.SET_NULL, null=True, blank=True
    )
    file_type = models.CharField(max_length=64)
    file_name = models.CharField(max_length=200)
    file_url = models.CharField(max_length=1000)
    thumbnail_url = models.CharField(max_length=1000)
    file_size = models.IntegerField()
