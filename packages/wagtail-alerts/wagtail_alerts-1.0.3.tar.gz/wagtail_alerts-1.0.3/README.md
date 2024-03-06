wagtail_alerts
==============

Simple wagtail alerts and toasts to programatically display or to create via settings inside of the wagtail admin.

Quick start
-----------

1. Add 'wagtail_alerts' and it's dependency' to your INSTALLED_APPS setting like this:

   ```
   INSTALLED_APPS = [
   ...,
   'wagtail_alerts',
       'globlocks',
   ]
   ```
2. Run `py ./manage.py collectstatic`
3. Run `py ./manage.py makemigrations` (We did not do this to prevent the wagtail 5/6 migration errors which might occur.)
4. Run `py ./manage.py migrate`
5. Add the template tags and scripts to your ``<body>``

   ```
   {% load wagtail_alerts_tags %}
   <link rel="stylesheet" href="{% url 'wagtail_alerts:css' %}"/>
   <script src="{% static 'wagtail_alerts/js/wagtail_alerts.js' %}"></script>
   {% wagtail_alerts container_class="fixed fixed-top" %}
   {% wagtail_alerts alert_type="TOAST" %}
   ```

## Custom Alert Types/Templates

You can add your own custom alert types by defining them in settings with `WAGTAIL_ALERTS_TYPES = [...]`

### Example settings

```
# settings.py
WAGTAIL_ALERTS_TYPES = [
    ("CUSTOM", _("Custom"), "myapp/blocks/my_alert_template.html", "myapp/templatetags/my_custom_list_template.html"),
]
```

### **Example list template**

We must then provide the HTML template to display the list of alerts.

```html
<!-- myapp/templatetags/my_custom_list_template.html -->
<div class="wagtail-alerts {{ CSS_VARIABLE_PREFIX }}custom-container {{ container_class }}">
    <div class="{{ CSS_VARIABLE_PREFIX }}custom-wrapper">
        {% for alert in alerts %}
            {% include_block alert with index=forloop.counter0 %}
        {% endfor %}
    </div>
</div>

```

#### List Template Context

We provide the following context for your custom alert type list template.

```
{{ alerts }}
{{ settings }}
{{ container_class }}
{{ CSS_VARIABLE_PREFIX }}
```

### Example Alert Template

Following that we can provide the alert template to render the individual alerts which have `alert_type="CUSTOM"`.

```
<!-- myapp/blocks/my_alert_template.html -->
<div class="{{CSS_VARIABLE_PREFIX}}custom-alert {{CSS_VARIABLE_PREFIX}}{{self.settings.alert_theme}}" id="alert-{{ index }}" data-duration="{{ self.settings.duration|default:0 }}" data-cookie-key="{{self.cookie_key}}"{% if self.once_per_session %} data-once{%endif%}{% if self.permanent_dismiss %} data-permanent-dismiss{%endif%}>
    <!-- Do something with these attributes! We do not implement this for you. -->
    <div class="custom-alert-content">
        {% if self.title %}
            <div class="alert-title">
                {{ self.get_title|safe }}:
            </div>
        {% endif %}
        <div class="alert-text">
            {{ self.get_body|safe }}
        </div>
    </div>
  
    <div class="dismissible-wrapper">
        {% if self.settings.dismissible %}
            <button type="button" class="alert-dismissible" aria-label="{% translate "Close" %}">×</button>
        {% endif %}
    </div>
</div>
{% endlocalize %}
```

#### Alert template context

For the full context of your alert template see `blocks.py`.

## Hooks

### Example usage of registering a custom alert from code

We provide hooks to allow you to add your own alerts to the alerts list.

This is useful if you want to add alerts based on some condition in your code.

```python
from wagtail_alerts.alert import Alert

@hooks.register('wagtail_alerts.construct_alerts')
def construct_alerts(request, base_list, settings):
    """
    Construct the alerts for the request.
    """

    ...

    if some_condition:
      base_list.append(Alert(
          title="This is a test alert",
          body="This is the test alert body",
          alert_theme="primary",
          dismissible=True,
          duration=5000,
          alert_type="TOAST",
      ))


```

### Example of changing the alert styles

We provide hooks to let you change the styles of the alerts.

This is useful if you want to change the colors of the alerts based on your theme.

```python
from wagtail import hooks


@hooks.register("wagtail_alerts.construct_styles")
def construct_styles(request, styles, settings):
    styles.change_color("primary", "#ff0000")
    styles.change_theme("dark", "#000000")
    styles.PRIMARY.text_color = "#ff0000"
    styles.PRIMARY.theme_color = "rgba(0, 0, 0, 0.5)"

```
