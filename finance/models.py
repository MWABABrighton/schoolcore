from decimal import Decimal

from django.db import models
from django.db.models import Sum


class FeeStructure(models.Model):

    FEE_TYPE_CHOICES = [
        ("TUITION", "Tuition"),
        ("OTHER", "Other"),
    ]

    academic_year = models.ForeignKey(
        "academics.AcademicYear",
        on_delete=models.PROTECT,
        related_name="fee_structures",
    )

    school_class = models.ForeignKey(
        "academics.SchoolClass",
        on_delete=models.PROTECT,
        related_name="fee_structures",
    )

    fee_type = models.CharField(
        max_length=20,
        choices=FEE_TYPE_CHOICES,
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    description = models.CharField(
        max_length=255,
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return (
            f"{self.academic_year} - "
            f"{self.school_class} - "
            f"{self.get_fee_type_display()} - "
            f"K{self.amount}"
        )


class StudentFee(models.Model):

    student = models.ForeignKey(
        "students.Student",
        on_delete=models.PROTECT,
        related_name="fees",
    )

    academic_year = models.ForeignKey(
        "academics.AcademicYear",
        on_delete=models.PROTECT,
        related_name="student_fees",
    )

    fee_structure = models.ForeignKey(
        FeeStructure,
        on_delete=models.PROTECT,
        related_name="student_fees",
    )

    amount_due = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "student",
                    "academic_year",
                    "fee_structure",
                ],
                name="unique_student_fee_structure",
            )
        ]

    @property
    def amount_paid(self):
        return self.payments.aggregate(
            total=Sum("amount")
        )["total"] or Decimal("0.00")

    @property
    def balance(self):
        return self.amount_due - self.amount_paid

    def __str__(self):
        return (
            f"{self.student} - "
            f"{self.academic_year} - "
            f"K{self.amount_due}"
        )


class Payment(models.Model):

    PAYMENT_METHOD_CHOICES = [
        ("CASH", "Cash"),
        ("BANK", "Bank Transfer"),
        ("MOBILE", "Mobile Money"),
        ("CARD", "Card"),
    ]

    student_fee = models.ForeignKey(
        StudentFee,
        on_delete=models.PROTECT,
        related_name="payments",
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    payment_date = models.DateField()

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
    )

    receipt_number = models.CharField(
        max_length=50,
        unique=True,
    )

    reference = models.CharField(
        max_length=100,
        blank=True,
    )

    recorded_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.PROTECT,
        related_name="recorded_payments",
    )

    remarks = models.CharField(
        max_length=255,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return (
            f"{self.receipt_number} - "
            f"{self.student_fee.student} - "
            f"K{self.amount}"
        )