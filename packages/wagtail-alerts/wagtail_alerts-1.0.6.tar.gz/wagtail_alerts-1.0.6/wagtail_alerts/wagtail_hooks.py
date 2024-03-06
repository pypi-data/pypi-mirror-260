from collections import OrderedDict as _OrderedDict
from typing import TYPE_CHECKING
from django.utils.translation import gettext_lazy as _
from django.http import HttpRequest

from wagtail import hooks

if TYPE_CHECKING:
    from .bases import BaseAlert
    from .models import AlertSettings


@hooks.register("wagtail_alerts.construct_alerts")
def _alerts_for_request_hook(request: "HttpRequest", alerts: list["BaseAlert"], settings: "AlertSettings") -> None:
    for alert in settings.alerts:
        alert: "BaseAlert" = alert.value
        alerts.append(alert)


