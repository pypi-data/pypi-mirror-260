from django.conf import settings
from django.utils.translation import gettext_lazy as _
from .bases import (
    TOAST,
    ALERT,
)


WAGTAIL_ALERTS_ALIGN = getattr(settings, "WAGTAIL_ALERTS_ALIGN", "flex-start")
COOKIE_KEY_PREFIX = getattr(settings, "WAGTAIL_ALERTS_COOKIE_KEY_PREFIX", "wagtail_alert_")
DEFAULT_TYPES = getattr(settings, "WAGTAIL_ALERTS_DEFAULT_TYPES", [
    (ALERT, _("Alert"), "wagtail_alerts/blocks/alert.html", "wagtail_alerts/tags/alerts.html"),
    (TOAST, _("Toast"), "wagtail_alerts/blocks/toast.html", "wagtail_alerts/tags/toasts.html"),
])
TYPES = getattr(settings, "WAGTAIL_ALERTS_TYPES", [])