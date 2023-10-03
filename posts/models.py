from django.db import models


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=128)
    body = models.TextField(max_length=8000)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    last_activity = models.DateTimeField(auto_now=True)
    actor = models.ForeignKey("messageboard.User", null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ["-last_activity"]

    def reply_count(self):
        return self.comment_set.count()


class Comment(models.Model):
    post = models.ForeignKey("posts.Post", on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    reply_to = models.ForeignKey(
        "posts.Comment", null=True, blank=True, on_delete=models.SET_NULL
    )
    actor = models.ForeignKey("messageboard.User", null=True, on_delete=models.SET_NULL)
    body = models.TextField(max_length=4000)
