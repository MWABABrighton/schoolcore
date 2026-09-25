from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path


urlpatterns = [
    path("", lambda request: redirect("dashboard_home")),

    path("admin/", admin.site.urls),
    path("reports/", include("reports.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("students/", include("students.urls")),
    path("finance/", include("finance.urls")),
    path("teachers/", include("teachers.urls")),
    path("accounts/", include("accounts.urls")),
    path("assessments/", include("assessments.urls")),
    path("attendance/", include("attendance.urls")),
    path("academics/", include("academics.urls")),
]