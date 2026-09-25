from django.urls import path

from . import views


urlpatterns = [
    path(
        "",
        views.attendance_home,
        name="attendance_home",
    ),

    path(
        "record/",
        views.record_attendance,
        name="record_attendance",
    ),

    path(
        "save/",
        views.save_attendance,
        name="save_attendance",
    ),

    path(
        "<int:attendance_id>/edit/",
        views.attendance_edit,
        name="attendance_edit",
    ),
]