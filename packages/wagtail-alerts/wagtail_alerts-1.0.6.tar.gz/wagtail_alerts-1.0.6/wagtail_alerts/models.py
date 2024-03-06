from django.utils.translation import gettext_lazy as _
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.settings.registry import register_setting
from wagtail.contrib.settings.models import BaseSiteSetting

from .blocks import AlertBlock

# Create your models here.
@register_setting
class AlertSettings(BaseSiteSetting):
    alerts = StreamField(
        [
            ("alert", AlertBlock()),
        ],
        use_json_field=True,
        blank=True,
        null=True,
    )

    panels = [
        FieldPanel("alerts"),
    ]

    class Meta:
        verbose_name = _("Alert Settings")
        verbose_name_plural = _("Alert Settings")
