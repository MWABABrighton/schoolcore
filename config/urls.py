from django.contrib import admin
from django.urls import include, path



urlpatterns = [
    path("admin/", admin.site.urls),
    path("reports/", include("reports.urls")),
     path("dashboard/", include("dashboard.urls")),
     path("students/", include("students.urls")),
     path("finance/", include("finance.urls")),
]