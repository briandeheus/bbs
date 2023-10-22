from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from messageboard.models import User


class BBSUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (
            None,
            {
                "fields": (
                    "display_name",
                    "avatar_url",
                    "mastodon_registration_date",
                    "mastodon_post_count",
                )
            },
        ),
    )


admin.site.register(User, BBSUserAdmin)
