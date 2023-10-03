"""

https://mastodon.example/oauth/authorize
?client_id=CLIENT_ID
&scope=read+write+push
&redirect_uri=urn:ietf:wg:oauth:2.0:oob
&response_type=code
"""
import http
import logging
from urllib.parse import urlencode

import requests
from django.conf import settings

from messageboard.exceptions import BBSException

log = logging.getLogger(__name__)
REDIRECT_URI = f"{settings.SITE_URL}/auth/confirm"


def protected_call(method, path, token, params=None):
    res = requests.request(
        method=method,
        url=f"{settings.MASTODON_URL}{path}",
        params=params,
        headers={"Authorization": f"Bearer {token}"},
    )
    return res.json()


def get_authorization_token(code: str) -> str:
    res = requests.post(
        f"{settings.MASTODON_URL}/oauth/token",
        params={
            "grant_type": "authorization_code",
            "code": code,
            "client_id": settings.MASTODON_CLIENT_KEY,
            "client_secret": settings.MASTODON_CLIENT_SECRET,
            "redirect_uri": REDIRECT_URI,
            "scope": "read",
        },
    )

    if res.status_code != http.HTTPStatus.OK:
        log.warning("Failed to retrieve authorization token: %s", res.text)
        raise BBSException(
            code="authorization_failed", message="Failed to get authorization token."
        )

    return res.json()["access_token"]


def get_authorization_url() -> str:
    params = {
        "client_id": settings.MASTODON_CLIENT_KEY,
        "scope": "read",
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
    }

    query_string = urlencode(params)
    base_url = settings.MASTODON_URL + "/oauth/authorize"
    return f"{base_url}?{query_string}"
