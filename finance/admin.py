from django.contrib import admin

from .models import FeeStructure, StudentFee, Payment


@admin.register(FeeStructure)
class FeeStructureAdmin(admin.ModelAdmin):

    list_display = (
        "academic_year",
        "school_class",
        "fee_type",
        "amount",
        "is_active",
    )

    list_filter = (
        "academic_year",
        "school_class",
        "fee_type",
        "is_active",
    )

    search_fields = (
        "school_class__name",
        "description",
    )


@admin.register(StudentFee)
class StudentFeeAdmin(admin.ModelAdmin):

    list_display = (
        "student",
        "academic_year",
        "fee_structure",
        "amount_due",
        "is_active",
    )

    list_filter = (
        "academic_year",
        "is_active",
    )

    search_fields = (
        "student__student_number",
        "student__first_name",
        "student__last_name",
    )

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = (
        "receipt_number",
        "student_fee",
        "amount",
        "payment_date",
        "payment_method",
        "recorded_by",
    )

    list_filter = (
        "payment_method",
        "payment_date",
    )

    search_fields = (
        "receipt_number",
        "reference",
        "student_fee__student__student_number",
        "student_fee__student__first_name",
        "student_fee__student__last_name",
    )

    date_hierarchy = "payment_date"