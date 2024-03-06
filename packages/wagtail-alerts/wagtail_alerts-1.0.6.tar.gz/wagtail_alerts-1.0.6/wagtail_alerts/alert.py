from collections import defaultdict
from functools import cached_property
from typing import TYPE_CHECKING
from django.http import HttpRequest
from django.template.loader import render_to_string
from wagtail import hooks
import hashlib

from .blocks import AlertBlockValue, AlertBlock
from .settings import COOKIE_KEY_PREFIX
from .bases import BaseAlert
from .alert_types import ALERT, AlertTypes

if TYPE_CHECKING:
    from .models import AlertSettings


def get_alerts(request: "HttpRequest", settings: "AlertSettings") -> dict[str, list["BaseAlert"]]:
    """
        Gets the alerts for the current request.
    """
    base_list: list["BaseAlert"] = []

    for hook in hooks.get_hooks('wagtail_alerts.construct_alerts'):
        hook(request, base_list, settings)

    d = defaultdict(list)

    # Filter the alerts and toasts.
    for alert in base_list:
        if (request.COOKIES.get(alert.cookie_key, "false") == "true" or
            not alert.is_active()):
            # Skip if dismissed or inactive.
            continue

        d[alert.get_alert_type()].append(alert)

    return d


class Alert(BaseAlert):
    """
    Represents an alert that can be rendered in a template.
    This alert can be shown to users using the "wagtail_alerts.construct_alerts" hook.
    """
    def __init__(self,
            title:              str,
            body:               str,
            alert_theme:         str = "primary",
            dismissible:        bool = True,
            duration:           int  = 0,
            alert_type:         str  = ALERT,
            once_per_session:   bool = False,
            permanent_dismiss:  bool = False
        ):
        self.title = title
        self.body = body
        self.alert_theme = alert_theme
        self.dismissible = dismissible
        self.duration = duration
        self.alert_type = alert_type
        self.once_per_session = once_per_session
        self.permanent_dismiss = permanent_dismiss

    def is_active(self):
        return True
    
    def get_alert_type(self):
        return self.alert_type
    
    @cached_property
    def cookie_key(self):
        s = [
            self.title,
            self.body,
            self.alert_type,
            self.duration,
            self.dismissible,
            self.alert_theme,
            self.once_per_session,
            self.permanent_dismiss,
        ]
        s = [str(i) for i in s]
        hash = hashlib.md5("".join(s).encode("utf-8")).hexdigest()
        return f"custom-{COOKIE_KEY_PREFIX}{hash}"

    def render_as_block(self, context: dict = None):
        context = context or {}
        value = AlertBlockValue(None, {
            "title": self.title,
            "body": self.body,
            "settings": {
                "duration": self.duration,
                "dismissible": self.dismissible,
                "alert_theme": self.alert_theme,
                "custom_template": self.alert_type,
                "once_per_session": self.once_per_session,
                "permanent_dismiss": self.permanent_dismiss,
                "dates": {
                    "active": True,
                }
            }
        })

        value.cookie_key = self.cookie_key

        context["self"] = value
        context[AlertBlock.TEMPLATE_VAR] = value
        alert_type = value.get_alert_type()
        typ = AlertTypes[alert_type]

        return render_to_string(typ.template, context, request=context.get("request", None))
    
