from datetime import datetime, timedelta
from typing import Optional

from django.utils import timezone

from messageboard.models import User


def str_to_timedelta(time_str: str) -> timedelta:
    units = time_str.split()
    kwargs = {units[i + 1]: int(units[i]) for i in range(0, len(units), 2)}
    return timedelta(**kwargs)


def can_post(
    user: User,
    min_posts_for_posting: Optional[int] = None,
    min_account_age_for_posting: Optional[str] = None,
) -> [bool, str]:
    if (
        min_posts_for_posting is not None
        and user.mastodon_post_count < min_posts_for_posting
    ):
        return [
            False,
            f"You need at least {min_posts_for_posting} posts on your Mastodon server to make a new post.",
        ]

    if min_account_age_for_posting:
        min_age_delta = str_to_timedelta(min_account_age_for_posting)

        if (timezone.now() - user.mastodon_registration_date) < min_age_delta:
            return [
                False,
                f"Account needs to be at least {min_account_age_for_posting} on your Mastodon server old to make a new post.",
            ]

    return [True, ""]


def can_comment(
    user: User,
    min_posts_for_commenting: Optional[int] = None,
    min_account_age_for_commenting: Optional[str] = None,
) -> [bool, str]:
    if (
        min_posts_for_commenting is not None
        and user.mastodon_post_count < min_posts_for_commenting
    ):
        return [False, f"Need {min_posts_for_commenting} posts to comment"]

    if min_account_age_for_commenting:
        min_age_delta = str_to_timedelta(min_account_age_for_commenting)
        if (datetime.now() - user.mastodon_registration_date) < min_age_delta:
            return [
                False,
                f"Account needs to be at least {min_account_age_for_commenting} old to comment",
            ]

    return [True, ""]
