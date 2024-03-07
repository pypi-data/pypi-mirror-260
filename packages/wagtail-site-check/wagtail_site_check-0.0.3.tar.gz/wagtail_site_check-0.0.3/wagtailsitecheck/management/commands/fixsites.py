from django.core.management.base import BaseCommand
from wagtail.models import Site

from wagtailsitecheck.defaults import ALLOWED_WAGTAIL_SITES


class Command(BaseCommand):
    help = "Interactively update sites with values defined in ALLOWED_WAGTAIL_SITES."

    def handle(self, *args, **options):
        for obj in Site.objects.all().order_by("hostname", "port"):
            allowed = ALLOWED_WAGTAIL_SITES
            site = f"{obj.hostname}:{obj.port}"
            if site not in allowed:
                question = f"{site} is not in ALLOWED_WAGTAIL_SITES. Specify a number to update the site."
                choices = "\n".join(
                    [f"{i + 1}: {site}" for i, site in enumerate(allowed)]
                )
                num = int(input(f"{question}\n\n{choices}\n\n"))

                obj.hostname, obj.port = allowed[num - 1].split(":")
                obj.save()

                print()
                print(f"Updated {site} -> {obj.hostname}:{obj.port}")
