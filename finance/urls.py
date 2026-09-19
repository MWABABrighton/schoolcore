from django.urls import path

from . import views


urlpatterns = [
    path("", views.finance_dashboard, name="finance_dashboard"),

    path(
        "payments/new/",
        views.record_payment,
        name="record_payment",
    ),
]