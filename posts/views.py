from django import views, forms
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone

from posts import methods as post_methods
from posts.models import Post, Comment


class SubmitForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "body"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["reply_to", "body"]


class ViewPost(views.View):
    def post(self, request, post_id):
        action = request.POST.get("action")
        post = Post.objects.get(pk=post_id)

        if action == "add-comment":
            comment = CommentForm(data=request.POST)

            comment.is_valid()
            comment.instance.post = post
            comment.instance.actor = request.user

            comment.save()

            post.last_activity = timezone.now()
            post.save()

        return self.get(request=request, post_id=post_id)

    def get(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        post.increment_views()
        return render(request, "posts/view.html", {"post": post})


# Create your views here.
class CreatePost(views.View):
    def post(self, request):
        form = SubmitForm(data=request.POST)
        [can_post, reason] = post_methods.can_post(
            user=request.user,
            min_posts_for_posting=settings.MIN_POSTS_FOR_POSTING,
            min_account_age_for_posting=settings.MIN_ACCOUNT_AGE_FOR_POSTING,
        )

        if not can_post:
            form.add_error(field=None, error=reason)

        form.instance.actor = request.user

        if not form.is_valid():
            return self.get(request=request, form=form)

        form.save()

        return redirect(to=reverse("post-view", kwargs={"post_id": form.instance.pk}))

    def get(self, request, form=None):
        return render(request, "posts/create.html", {"form": form})
