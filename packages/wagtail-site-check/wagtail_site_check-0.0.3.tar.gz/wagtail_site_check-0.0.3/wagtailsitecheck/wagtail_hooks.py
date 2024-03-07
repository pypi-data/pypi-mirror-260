from typing import Any, Mapping

from wagtail.admin.ui.components import Component
from wagtail.models import Site

from wagtailsitecheck.defaults import ALLOWED_WAGTAIL_SITES


class SiteCheckNotificationPanel(Component):
    name = "site_check_notification"
    template_name = "wagtailsitecheck/site_check_notification.html"
    order = 0

    def get_context_data(self, *args) -> Mapping[str, Any]:
        disallowed_sites = []
        for obj in Site.objects.all().order_by("hostname", "port"):
            site = f"{obj.hostname}:{obj.port}"
            if site not in ALLOWED_WAGTAIL_SITES:
                disallowed_sites.append((site, obj.pk))

        return {
            "allowed_sites": ALLOWED_WAGTAIL_SITES,
            "disallowed_sites": disallowed_sites,
        }
