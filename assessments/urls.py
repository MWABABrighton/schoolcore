from django.urls import path

from . import views


urlpatterns = [
    path(
        "",
        views.assessment_home,
        name="assessment_home",
    ),

    path(
        "examinations/new/",
        views.create_examination,
        name="create_examination",
    ),

    path(
        "examinations/",
        views.teacher_examinations,
        name="teacher_examinations",
    ),

    path(
        "examinations/<int:examination_id>/marks/",
        views.enter_marks,
        name="enter_marks",
    ),
]