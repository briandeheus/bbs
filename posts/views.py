from django import views, forms
from django.shortcuts import render
from django.utils import timezone

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
        return render(request, "posts/view.html", {"post": post})


# Create your views here.
class CreatePost(views.View):
    def post(self, request):
        form = SubmitForm(data=request.POST)
        form.instance.actor = request.user

        form.is_valid()
        form.save()

        return self.get(request=request)

    def get(self, request):
        return render(request, "posts/create.html")
