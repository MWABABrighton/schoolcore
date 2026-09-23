from django.urls import path

from . import views


urlpatterns = [
    path("", views.finance_dashboard, name="finance_dashboard"),

    path(
        "payments/new/",
        views.record_payment,
        name="record_payment",
    ),

    path(
        "payments/",
        views.payment_list,
        name="payment_list",
    ),

    path(
    "student/<int:student_id>/",
    views.student_finance,
    name="student_finance",
    ),

    path(
    "payments/<int:payment_id>/",
    views.payment_detail,
    name="payment_detail",
    ),

    

    path(
    "fee-structures/new/",
    views.create_fee_structure,
    name="create_fee_structure",
    ),
]