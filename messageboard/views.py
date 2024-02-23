from django.contrib.auth import login, logout
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from messageboard.models import User
from messageboard.utils.oauth import (
    get_authorization_token,
    get_authorization_url,
    protected_call,
)
from posts.models import Post


class Landing(View):
    def get(self, request):
        posts = Post.objects.all().order_by("-pinned", "-last_activity")
        paginator = Paginator(posts, 10)  # Show 10 posts per page
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(
            request=request,
            template_name="messageboard/landing.html",
            context={"page_obj": page_obj},
        )


class Search(View):
    def get(self, request):
        query = request.GET.get("query")
        posts = Post.objects.search(query=request.GET.get("query"))
        paginator = Paginator(posts, 10)  # Show 10 posts per page
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(
            request=request,
            template_name="messageboard/landing.html",
            context={"page_obj": page_obj, "query": query},
        )


class NewPosts(View):
    def get(self, request):
        posts = Post.objects.all().order_by("-created_on")
        paginator = Paginator(posts, 10)  # Show 10 posts per page
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(
            request=request,
            template_name="messageboard/landing.html",
            context={"page_obj": page_obj},
        )


class Login(View):
    def get(self, request):
        return render(request=request, template_name="messageboard/login.html")


class Logout(View):
    def get(self, request):
        logout(request=request)
        return redirect(to=reverse("landing"))


class Confirm(View):
    def get(self, request):
        code = request.GET.get("code")
        token = get_authorization_token(code=code)
        user = protected_call(
            method="get", path="/api/v1/accounts/verify_credentials", token=token
        )

        user_id = user["id"]
        display_name = user["display_name"]
        avatar_url = user["avatar_static"]
        profile_url = user["url"]
        registration_date = user["created_at"]
        post_count = user["statuses_count"]

        try:
            user = User.objects.get(username=user_id)
        except User.DoesNotExist:
            user = User.objects.create(
                username=user_id,
                display_name=display_name,
                authorization_token=token,
                avatar_url=avatar_url,
                profile_url=profile_url,
                mastodon_registration_date=registration_date,
            )

        user.mastodon_post_count = post_count
        user.save()

        login(request=request, user=user)

        return redirect(to=reverse("landing"))


class Authorize(View):
    def get(self, request):
        return redirect(to=get_authorization_url())
