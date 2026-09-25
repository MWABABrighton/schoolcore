from django.urls import path

from . import views


urlpatterns = [

    path(
        "",
        views.reports_home,
        name="reports_home",
    ),

    path(
        "student/<int:student_id>/",
        views.student_report_card,
        name="student_report_card",
    ),

    path(
        "my-class/",
        views.my_class_reports,
        name="my_class_reports",
    ),

    path(
        "my-class/<int:assignment_id>/",
        views.class_report_cards,
        name="class_report_cards",
    ),
    path(
    "my-class/<int:assignment_id>/print/",
    views.print_class_report_cards,
    name="print_class_report_cards",
    ),

]