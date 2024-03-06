from django.shortcuts import render
from django.http import HttpResponseNotAllowed
from django.utils.translation import gettext_lazy as _
from django.contrib import messages

from wagtail import hooks

from .settings import (
    WAGTAIL_ALERTS_ALIGN,
)
from wagtail_alerts import (
    WagtailAlertStyles,
    CSS_VARIABLE_PREFIX,
)
from .models import AlertSettings



# Create your views here.
def render_alerts_css(request):
    """
        Renders the CSS for the alerts.
    """

    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])

    styles = WagtailAlertStyles()
    settings = AlertSettings.for_request(request)

    for hook in hooks.get_hooks("wagtail_alerts.construct_styles"):
        hook(request=request, styles=styles, settings=settings)

    return render(
        request,
        "wagtail_alerts/views/alerts.css",
        {
            "styles": styles,
            "settings": settings,
            "ALIGN_ALERTS": WAGTAIL_ALERTS_ALIGN,
            "CSS_VARIABLE_PREFIX": CSS_VARIABLE_PREFIX,
        },
        content_type="text/css",
    )
