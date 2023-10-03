"""
URL configuration for messageboard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from messageboard.views import Authorize, Confirm, Landing
from posts.views import CreatePost, ViewPost

urlpatterns = [
    path("", Landing.as_view(), name="landing"),
    path("auth/authorize", Authorize.as_view(), name="authorize"),
    path("auth/confirm", Confirm.as_view(), name="confirm"),
    path("posts/create", CreatePost.as_view(), name="post-create"),
    path("posts/<int:post_id>", ViewPost.as_view(), name="post-view"),
    path("admin/", admin.site.urls),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
