from django.http import HttpRequest
from django.template import Library
from django.template.loader import render_to_string

from .. import (
    CSS_VARIABLE_PREFIX,
    alert,
    alert_types,
)
from ..models import AlertSettings


register = Library()


@register.simple_tag(takes_context=True)
def wagtail_alerts(context, container_class: str = "absolute", alert_type: str = alert_types.ALERT):
    """
    Renders the alerts for the current request.

    Caches the alerts in the context dictionary so that they are only computed once per request.
    """
    request: HttpRequest = context['request']
    settings = AlertSettings.for_request(request)

    wagtail_alerts = context.get("WAGTAIL_ALERTS")
    typ = alert_types.AlertTypes[alert_type]

    if wagtail_alerts is None:
        wagtail_alerts = alert.get_alerts(
            request=request,
            settings=settings,
        )

    context['WAGTAIL_ALERTS'] = wagtail_alerts

    return render_to_string(typ.list_template, context={
        'alerts': wagtail_alerts[alert_type],
        'settings': settings,
        'container_class': container_class,
        'CSS_VARIABLE_PREFIX': CSS_VARIABLE_PREFIX,
    })
