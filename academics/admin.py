from django.contrib import admin
from .models import AcademicYear, SchoolClass, Section, Subject


@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ("year", "is_current")
    list_filter = ("is_current",)
    search_fields = ("year",)


@admin.register(SchoolClass)
class SchoolClassAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ("name", "school_class")
    list_filter = ("school_class",)
    search_fields = ("name", "school_class__name")


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "is_active")
    list_filter = ("is_active",)
    search_fields = ("code", "name")