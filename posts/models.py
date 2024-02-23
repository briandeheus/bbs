from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db import models
from django.db.models import F


# Custom QuerySet
class PostQuerySet(models.QuerySet):
    def search(self, query):
        vector = SearchVector("title", weight="A") + SearchVector("body", weight="B")
        query = SearchQuery(query)
        return (
            self.annotate(rank=SearchRank(vector, query))
            .filter(rank__gte=0.1)
            .order_by("-rank")
        )


# Custom Manager
class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)

    def search(self, query):
        return self.get_queryset().search(query)


# Create your models here.
class Post(models.Model):
    objects = PostManager()

    title = models.CharField(max_length=128)
    body = models.TextField(max_length=8000)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    last_activity = models.DateTimeField(auto_now=True)
    actor = models.ForeignKey("messageboard.User", null=True, on_delete=models.SET_NULL)
    pinned = models.BooleanField(default=False)
    views = models.IntegerField(default=0)
    media = models.ManyToManyField("media.Media")

    class Meta:
        ordering = ["-last_activity"]

    def reply_count(self):
        return self.comment_set.count()

    def increment_views(self):
        self.views = F("views") + 1
        self.save(update_fields=["views"])


class Comment(models.Model):
    post = models.ForeignKey("posts.Post", on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    reply_to = models.ForeignKey(
        "posts.Comment", null=True, blank=True, on_delete=models.SET_NULL
    )
    actor = models.ForeignKey("messageboard.User", null=True, on_delete=models.SET_NULL)
    body = models.TextField(max_length=4000)
