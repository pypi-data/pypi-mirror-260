from django.utils.translation import gettext_lazy as _

from globlocks.colors import to_rgb

CSS_VARIABLE_PREFIX = "wagtail-alerts-"

class WagtailAlertTheme:
    css_variable_prefix = CSS_VARIABLE_PREFIX

    def __init__(self, css_variable_name: str, label: str, text_color: str, theme_color: str):
        self.css_variable_name = css_variable_name
        self.label = label
        self.set_color(text_color)
        self.set_theme(theme_color)
        self.custom: list[str] = []
        self.colors = (
            ("text", "text_color"),
            ("rgb-text", "_text_color_rgb"),
            ("r-text", "_text_color_r"),
            ("g-text", "_text_color_g"),
            ("b-text", "_text_color_b"),
            ("a-text", "_text_color_a"),

            ("theme", "theme_color"),
            ("rgb-theme", "_theme_color_rgb"),
            ("r-theme", "_theme_color_r"),
            ("g-theme", "_theme_color_g"),
            ("b-theme", "_theme_color_b"),
            ("a-theme", "_theme_color_a"),
        )

    def add_custom(self, css_format_str: str):
        self.custom.append(css_format_str)

    def get_custom(self):
        l = []
        for c in self.custom:
            c = c.format(
                prefix=self.css_variable_prefix,
                name=self.css_variable_name,
                label=self.label,
                text_color=self.text_color,
                theme_color=self.theme_color,
                rgb_text=self._text_color_rgb,
                r_text=self._text_color_r,
                g_text=self._text_color_g,
                b_text=self._text_color_b,
                a_text=self._text_color_a,
                rgb_theme=self._theme_color_rgb,
                r_theme=self._theme_color_r,
                g_theme=self._theme_color_g,
                b_theme=self._theme_color_b,
                a_theme=self._theme_color_a,
            )
            l.append(c)
        return "\n".join(l)

    def set_color(self, color: str):
        self._text_color = color
        self._itext_color_rgb = to_rgb(color, as_string=False, preserve_alpha=True, default_alpha=1)
        self._text_color_rgb = ",".join(str(c) for c in self._itext_color_rgb)
        self._text_color_r, self._text_color_g, self._text_color_b, self._text_color_a = self._itext_color_rgb

    def set_theme(self, color: str):
        self._theme_color = color
        self._itheme_color_rgb = to_rgb(color, as_string=False, preserve_alpha=True, default_alpha=1)
        self._theme_color_rgb = ",".join(str(c) for c in self._itheme_color_rgb)
        self._theme_color_r, self._theme_color_g, self._theme_color_b, self._theme_color_a = self._itheme_color_rgb

    @property
    def text_color(self):
        return self._text_color
    
    @text_color.setter
    def text_color(self, value):
        self.set_color(value)

    @property
    def theme_color(self):
        return self._theme_color
    
    @theme_color.setter
    def theme_color(self, value):
        self.set_theme(value)

    @property
    def name(self):
        return self.css_variable_name

    @property
    def css_variable(self):
        return f"{self.css_variable_prefix}{self.css_variable_name}"

    def __str__(self):
        s = []
        for kwarg, attr in self.colors:
            s.append(f"    --{self.css_variable}-{kwarg}: {getattr(self, attr)};")
        return "\n".join(s)

class WagtailAlertStylesMeta(type):
    def __new__(cls, name, bases, attrs):

        attrs["choices"] = (
            (c[0], c[1]) for c in attrs["colors"]
        )

        return super().__new__(cls, name, bases, attrs)

class WagtailAlertStyles(metaclass=WagtailAlertStylesMeta):
    """
        A class to store the different alert styles.
    """

    choices: tuple[tuple[str, str]]

    colors = (
        ("primary", _("Primary"), "#004085", "#b8daff"),
        ("secondary", _("Secondary"), "#383d41", "#d6d8db"),
        ("success", _("Success"), "#155724", "#c3e6cb"),
        ("danger", _("Danger"), "#721c24", "#f8d7da"),
        ("warning", _("Warning"), "#856404", "#fff3cd"),
        ("info", _("Info"), "#0c5460", "#d1ecf1"),
        ("light", _("Light"), "#818182", "#fefefe"),
        ("dark", _("Dark"), "#1b1e21", "#d6d8d9"),
    )

    def __init__(self):
        colors = list(self.colors)
        color_dict = {}
        for i, alert in enumerate(colors):
            alert_theme = WagtailAlertTheme(*alert)
            setattr(self, alert_theme.css_variable_name, alert_theme)
            setattr(self, alert_theme.css_variable_name.upper(), alert_theme)
            color_dict[alert_theme.css_variable_name] = alert_theme
            colors[i] = alert_theme

        self.colors = colors
        self.color_dict = color_dict

    def change_color(self, alert_theme: str, color: str):
        alert = self[alert_theme]
        alert.text_color = color

    def change_theme(self, alert_theme: str, color: str):
        alert = self[alert_theme]
        alert.theme_color = color

    def __getitem__(self, item) -> WagtailAlertTheme:
        if isinstance(item, int):
            return self.colors[item]
        
        return self.color_dict[item]
    
