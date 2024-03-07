from django.conf import settings

ALLOWED_WAGTAIL_SITES = getattr(settings, "ALLOWED_WAGTAIL_SITES", None)


def get_allowed_wagtail_sites():
    return list([f"{site}:443" for site in settings.ALLOWED_HOSTS])


if ALLOWED_WAGTAIL_SITES is None:
    ALLOWED_WAGTAIL_SITES = get_allowed_wagtail_sites()
