from abc import (
    ABC as _ABC, 
    abstractproperty as _abstractproperty, 
    abstractmethod as _abstractmethod
)


TOAST = "TOAST"
ALERT = "ALERT"


class BaseAlert(_ABC):
    """
        Your custom alert type should minimally implement this API.

        - `cookie_key: str` - A unique key for the alert. This is used to store the alert's state in a cookie (wether it has been dismissed or not).
        - `is_active() -> bool` - Returns True if the alert should be shown to the user.
        - `get_alert_type() -> str` - Returns a unique key for the alert.
            - This is used to determine what type of alert it is (e.g. toast, alert).
        - `render_as_block(context: dict = None) -> str` - Renders the alert as a block of HTML.
    """

    @_abstractproperty
    def cookie_key(self) -> str:
        """This should be implemented as a cached_property by subclasses to prevent unnecessary computation."""

    @_abstractmethod
    def is_active(self) -> bool:
        """Returns True if the alert should be shown to the user. This might be called multiple times."""

    @_abstractmethod
    def get_alert_type(self) -> str:
        """Returns a unique key for the alert, this is used to determine what type of alert it is (e.g. toast, alert)."""

    @_abstractmethod
    def render_as_block(self, context: dict = None) -> str:
        """Renders the alert as a block of HTML, this is called once per request upon rendering the alerts."""
