from django.urls import path

from . import views


urlpatterns = [
    path(
        "",
        views.academics_home,
        name="academics_home",
    ),

    path(
        "academic-years/new/",
        views.create_academic_year,
        name="create_academic_year",
    ),

    path(
        "classes/new/",
        views.create_class,
        name="create_class",
    ),

    path(
        "sections/new/",
        views.create_section,
        name="create_section",
    ),

    path(
        "subjects/new/",
        views.create_subject,
        name="create_subject",
    ),
]