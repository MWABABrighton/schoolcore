from django.urls import path

from . import views


urlpatterns = [
    path(
        "student/<int:student_id>/",
        views.student_report_card,
        name="student_report_card",
    ),
]