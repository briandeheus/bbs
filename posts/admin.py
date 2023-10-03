from django.contrib import admin

from .models import Post


# Post Admin
class PostAdmin(admin.ModelAdmin):
    autocomplete_fields = ["actor"]
    list_display = ["title", "actor"]


admin.site.register(Post, PostAdmin)
