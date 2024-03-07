from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand
from wagtail.models import Site

from wagtailsitecheck.defaults import ALLOWED_WAGTAIL_SITES


class Command(BaseCommand):
    help = "Update sites with values defined in ALLOWED_WAGTAIL_SITES."

    def handle(self, *args, **options):
        for obj in Site.objects.all().order_by("hostname", "port"):
            site = f"{obj.hostname}:{obj.port}"
            if site not in ALLOWED_WAGTAIL_SITES:
                raise ImproperlyConfigured(
                    f"{site} is not in ALLOWED_WAGTAIL_SITES. "
                    f"Update via 'Admin -> Settings -> Sites', "
                    f"or run `fixsites` management command."
                )
