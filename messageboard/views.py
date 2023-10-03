from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from messageboard.models import User
from messageboard.utils.oauth import get_authorization_url, get_authorization_token, protected_call
from posts.models import Post


class Landing(View):

    def get(self, request):
        posts = Post.objects.all()
        return render(request=request, template_name="messageboard/landing.html", context={"posts": posts})


class Login(View):

    def get(self, request):
        return render(request=request, template_name="messageboard/login.html")


class Confirm(View):
    def get(self, request):
        code = request.GET.get("code")
        token = get_authorization_token(code=code)
        user = protected_call(method="get", path="/api/v1/accounts/verify_credentials", token=token)

        user_id = user["id"]
        display_name = user["display_name"]
        avatar_url = user["avatar_static"]
        profile_url = user["url"]

        try:
            user = User.objects.get()
        except User.DoesNotExist:
            user = User.objects.create(
                username=user_id,
                display_name=display_name,
                avatar_url=avatar_url,
                profile_url=profile_url
            )

        login(request=request, user=user)

        return redirect(to=reverse("landing"))


class Authorize(View):

    def get(self, request):
        return redirect(to=get_authorization_url())
