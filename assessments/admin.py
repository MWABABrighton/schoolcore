from django.contrib import admin

from .models import Examination, Result


@admin.register(Examination)
class ExaminationAdmin(admin.ModelAdmin):

    list_display = [
        "academic_year",
        "term",
        "class_section",
        "subject",
        "exam_date",
        "is_active",
    ]

    list_filter = [
        "academic_year",
        "term",
        "class_section",
        "subject",
        "is_active",
    ]

    search_fields = [
        "class_section__name",
        "subject__name",
    ]


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):

    list_display = [
        "student",
        "examination",
        "marks",
        "recorded_by",
    ]

    list_filter = [
        "examination__academic_year",
        "examination__term",
        "examination__class_section",
        "examination__subject",
    ]

    search_fields = [
        "student__student_number",
        "student__first_name",
        "student__last_name",
    ]