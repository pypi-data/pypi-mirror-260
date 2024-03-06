from functools import cached_property
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from wagtail import blocks
from wagtail.templatetags.wagtailcore_tags import richtext

from globlocks.blocks import (
    TemplateBlock,
    TemplateBlockConfiguration,
    BaseBlockConfiguration,
    RangeSliderBlock,
)

from wagtail_alerts import (
    WagtailAlertStyles,
    CSS_VARIABLE_PREFIX,
)
from .bases import (
    ALERT,
    BaseAlert,
)
from .alert_types import (
    AlertTypes,
)
from .settings import (
    COOKIE_KEY_PREFIX,
)

import hashlib


class AlertDatesBlockConfigurationValue(blocks.StructValue):
    def is_active(self):
        active_from = self.get("active_from")
        active_to = self.get("active_to")

        if active_from and active_from > timezone.now():
            return False

        if active_to and active_to < timezone.now():
            return False
        
        if active_from and active_to:
            return active_from < timezone.now() < active_to
        
        return self.get("active")
    
class AlertDatesBlockConfiguration(BaseBlockConfiguration):
    active_from = blocks.DateTimeBlock(
        label=_("Active From"),
        help_text=_("The date and time the alert should start being displayed."),
        required=False,
    )

    active_to = blocks.DateTimeBlock(
        label=_("Active To"),
        help_text=_("The date and time the alert should stop being displayed."),
        required=False,
    )

    active = blocks.BooleanBlock(
        label=_("Active"),
        help_text=_("Whether the alert is active. If not active, the alert will not be displayed."),
        default=True,
        required=False,
    )

    class Meta:
        label = _("Active From/To Dates")
        button_label = _("Active Configuration")
        icon = "date"
        form_template = "wagtail_alerts/blocks/forms/alert_dates_settings.html"
        value_class = AlertDatesBlockConfigurationValue
        

class AlertBlockConfiguration(TemplateBlockConfiguration):
    duration = RangeSliderBlock(
        label=_("Duration"),
        help_text=_("The alert will display for this many milliseconds.%(linebreak)s1000ms = 1s%(linebreak)s0ms = infinite.") % {
            "linebreak": "<br>"
        },
        unit="ms",
        stepping=500,
        default=0,
        min_value=0,
        max_value=25 * 1000,
    )

    dismissible = blocks.BooleanBlock(
        label=_("Dismissible"),
        help_text=_("Can the alert be dismissed by the user?"),
        default=True,
        required=False,
    )

    alert_theme = blocks.ChoiceBlock(
        label=_("Type"),
        help_text=_("The type/theme of alert to display."),
        choices=WagtailAlertStyles.choices,
        default="primary",
    )

    once_per_session = blocks.BooleanBlock(
        label=_("Once Per Session"),
        help_text=_("Whether to only show the alert once per session, it will not show after a page refresh for up to a day."),
        default=False,
        required=False,
    )

    permanent_dismiss = blocks.BooleanBlock(
        label=_("Permanent Dismiss"),
        help_text=_("If this is true the alert will not be displayed for a day if the user dismisses it."),
        default=True,
        required=False,
    )

    dates = AlertDatesBlockConfiguration(
        label=_("Active Settings"),
        required=False,
    )

    class Meta:
        label = _("Alert Settings")
        button_label = _("Open Alert Settings")
        form_template = "wagtail_alerts/blocks/forms/alert_settings.html"
        icon = "warning"

class AlertBlockValue(blocks.StructValue):
    
    def get_title(self):
        return self.get("title")
    
    def get_body(self):
        return str(richtext(self.get("body")))
    
    def permanent_dismiss(self):
        return self.get("settings").get("permanent_dismiss")
    
    def once_per_session(self):
        return self.get("settings").get("once_per_session")
    
    @cached_property
    def cookie_key(self):
        return f"{COOKIE_KEY_PREFIX}{self.get_alert_hash()}"
    
    def is_active(self):
        settings = self.get("settings")
        dates = settings.get("dates")
        return dates.is_active()

    def get_alert_type(self):
        return self.get('settings').get('custom_template', ALERT)

    def get_alert_hash(self):
        s = [
            self.get_title(),
            self.get_body(),
            self.get_alert_type(),
            self.get("settings").get("duration"),
            self.get("settings").get("dismissible"),
            self.get("settings").get("alert_theme"),
            self.get("settings").get("once_per_session"),
            self.get("settings").get("permanent_dismiss"),
            self.get("settings").get("dates").get("active_from"),
            self.get("settings").get("dates").get("active_to"),
            self.get("settings").get("dates").get("active"),
        ]
        s = [str(i) for i in s]
        return hashlib.md5("".join(s).encode("utf-8")).hexdigest()
    

class AlertBlock(TemplateBlock):
    templates = AlertTypes.choices

    advanced_settings_class = AlertBlockConfiguration

    title = blocks.CharBlock(
        label=_("Title"),
        required=False,
    )

    body = blocks.RichTextBlock(
        label=_("Body"),
        required=True,
    )

    class Meta:
        label = _("Alert")
        icon = "warning"
        group = _("Alerts")
        template = "wagtail_alerts/blocks/alert.html"
        value_class = AlertBlockValue

    def get_context(self, value, parent_context=None):
        return super().get_context(value, parent_context) | {
            "CSS_VARIABLE_PREFIX": CSS_VARIABLE_PREFIX,
        }
