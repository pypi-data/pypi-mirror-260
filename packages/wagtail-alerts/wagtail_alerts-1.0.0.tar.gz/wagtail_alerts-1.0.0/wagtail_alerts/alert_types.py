from typing import Any as _Any, Iterable as _Iterable, OrderedDict as _ODT
from collections import OrderedDict as _OrderedDict
from django.utils.module_loading import import_string as _import_string
from .bases import (
    ALERT,
)
from .settings import (
    DEFAULT_TYPES,
    TYPES,
)

class AlertType:
    """
        A class that represents an alert type.

        - `key: str` - A unique key for the alert type.
        - `label: str` - A human-readable label for the alert type.
        - `description: str` - A human-readable description for the alert type.
    """

    def __init__(self, key: str, label: str, template: str, list_template: str = None):
        self.key = key
        self.label = label
        self.template = template
        self.list_template = list_template or template

    def __hash__(self) -> int:
        return hash(self.key)

def _import_if_str(value: _Any) -> _Any:
    """
        If the value is a string, import it as a dotted path.

        - `value: Any` - The list of alert type definitions to import.
    """
    if isinstance(value, str):
        return _import_string(value)
    return value


def _get_alert_types() -> _Iterable[AlertType]:
    """
        Get all alert types.

        - Returns: A list of alert types.
    """
    _default_types = _import_if_str(DEFAULT_TYPES)
    _types = _import_if_str(TYPES)
    for args in _default_types + _types:
        yield AlertType(*args)


class _AlertTypes(_OrderedDict):
    """
        A dictionary of alert types.
    """

    DEFAULT_KEY: str = ALERT

    @property
    def choices(self: _ODT[str, AlertType]) -> list[tuple[str, str, str]]:
        return [(key, alert_type.template, alert_type.label) for key, alert_type in self.items()]
    
    @property
    def default(self) -> AlertType:
        return self[self.DEFAULT_KEY]
    
    def __getitem__(self, key: str) -> AlertType:
        return super().__getitem__(key)
    
    def get(self, key: str, default: _Any = None, fail_silently: bool = False) -> AlertType:
        if fail_silently:
            if isinstance(default, str):
                default = self.get(default)
            return super().get(key, default)
        
        if key not in self:
            raise KeyError(f"Unknown alert type: {key}")

        return super().get(key, self[self.DEFAULT_KEY])

AlertTypes: _ODT[str, AlertType] = _AlertTypes()

for alert_type in _get_alert_types():
    AlertTypes[alert_type.key] = alert_type

del _get_alert_types
del _import_string
del _import_if_str
del _AlertTypes
del _ODT
del _Any
del _Iterable
del _OrderedDict
