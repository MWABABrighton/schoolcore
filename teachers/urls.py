from django.urls import path

from . import views


urlpatterns = [
    path(
        "",
        views.teacher_list,
        name="teacher_list",
    ),

    path(
        "new/",
        views.teacher_create,
        name="teacher_create",
    ),


    path(
    "class-teacher/new/",
    views.class_teacher_assignment_create,
    name="class_teacher_assignment_create",
    ),    
]