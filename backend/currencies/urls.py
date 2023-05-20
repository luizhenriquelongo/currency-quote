from django.urls import (
    path,
)
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView

from currencies.api import views as currencies_views

urlpatterns = [
    path("rates/", currencies_views.get_rates, name="rates-list-api"),
    path("docs/", SpectacularRedocView.as_view(url_name="schema"), name="redocs-ui"),
    path("docs/schema/", SpectacularAPIView.as_view(), name="schema"),
]
