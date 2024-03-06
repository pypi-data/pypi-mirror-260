from django.urls import path
from .views import render_alerts_css

app_name = "wagtail_alerts"

urlpatterns = [
    path("alerts.css", render_alerts_css, name="css"),
]