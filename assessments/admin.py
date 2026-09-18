from django.contrib import admin
from .models import Examination, Result


@admin.register(Examination)
class ExaminationAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "academic_year",
        "term",
        "start_date",
        "end_date",
        "is_active",
    )

    list_filter = (
        "academic_year",
        "term",
        "is_active",
    )

    search_fields = (
        "name",
    )


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "examination",
        "subject",
        "marks",
        "recorded_by",
    )

    list_filter = (
        "examination",
        "subject",
    )

    search_fields = (
        "student__student_number",
        "student__first_name",
        "student__last_name",
        "subject__name",
    )