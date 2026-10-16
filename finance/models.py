
# Import Decimal to handle monetary values accurately.
# This avoids floating-point rounding errors when calculating fees.
from decimal import Decimal

# Import Django's models module to define database tables and fields.
from django.db import models

# Import Sum to calculate the total amount paid by a student.
from django.db.models import Sum


# ============================================================
# FEE STRUCTURE MODEL
# Defines the fees charged for each class in an academic year.
# Example: Grade 8 tuition fee for the 2026 academic year.
# ============================================================
class FeeStructure(models.Model):

    # Define the available categories of school fees.
    # The first value is stored in the database.
    # The second value is displayed to users.
    FEE_TYPE_CHOICES = [
        ("TUITION", "Tuition"),
        ("OTHER", "Other"),
    ]

    # Link the fee structure to an academic year.
    # PROTECT prevents deleting an academic year that is in use.
    # related_name allows access through academic_year.fee_structures.
    academic_year = models.ForeignKey(
        "academics.AcademicYear",
        on_delete=models.PROTECT,
        related_name="fee_structures",
    )

    # Link the fee structure to a school class.
    # PROTECT prevents deleting a class that has associated fee structures.
    # related_name allows access through school_class.fee_structures.
    school_class = models.ForeignKey(
        "academics.SchoolClass",
        on_delete=models.PROTECT,
        related_name="fee_structures",
    )

    # Store the category of fee, such as Tuition or Other.
    # The available values are restricted by FEE_TYPE_CHOICES.
    fee_type = models.CharField(
        max_length=20,
        choices=FEE_TYPE_CHOICES,
    )

    # Store the fee amount using a decimal field.
    # max_digits=12 allows up to 12 digits in total.
    # decimal_places=2 allows two digits after the decimal point.
    # Suitable for storing monetary amounts such as ZMW fees.
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    # Store an optional description of the fee.
    # blank=True means the field can be left empty in forms.
    description = models.CharField(
        max_length=255,
        blank=True,
    )

    # Indicate whether this fee structure is currently active.
    # New fee structures are active by default.
    is_active = models.BooleanField(
        default=True,
    )

    # Automatically record the date and time when the record is created.
    # Django sets this value only when the record is first saved.
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    # Automatically update the date and time whenever the record is saved.
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    # Define rules and settings for this model.
    class Meta:

        # Prevent duplicate fee structures for the same academic year,
        # school class, and fee type.
        # For example, the same class cannot have two Tuition structures
        # for the same academic year.
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "academic_year",
                    "school_class",
                    "fee_type",
                ],
                name="unique_fee_structure_per_class_year_type",
            )
        ]

    # Return a readable description when a fee structure is displayed.
    # get_fee_type_display() returns the human-readable fee category.
    def __str__(self):
        return (
            f"{self.academic_year} - "
            f"{self.school_class} - "
            f"{self.get_fee_type_display()} - "
            f"K{self.amount}"
        )


# ============================================================
# STUDENT FEE MODEL
# Records the amount a particular student owes for an academic year.
# It connects a student to the applicable fee structure.
# ============================================================
class StudentFee(models.Model):

    # Link this fee record to a student.
    # PROTECT prevents deleting a student who has an associated fee record.
    # related_name allows access through student.fees.
    student = models.ForeignKey(
        "students.Student",
        on_delete=models.PROTECT,
        related_name="fees",
    )

    # Link the student's fee record to an academic year.
    # PROTECT prevents deleting an academic year that is in use.
    # related_name allows access through academic_year.student_fees.
    academic_year = models.ForeignKey(
        "academics.AcademicYear",
        on_delete=models.PROTECT,
        related_name="student_fees",
    )

    # Link the student fee to the fee structure used to calculate the fee.
    # This identifies the class fee structure associated with the student.
    # PROTECT prevents deleting a fee structure that is in use.
    # related_name allows access through fee_structure.student_fees.
    fee_structure = models.ForeignKey(
        FeeStructure,
        on_delete=models.PROTECT,
        related_name="student_fees",
    )

    # Store the total amount the student is expected to pay.
    # This is kept separately from the fee structure amount so the
    # student's recorded amount due can remain unchanged if the
    # general fee structure is changed later.
    amount_due = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    # Indicate whether this student's fee record is active.
    # New student fee records are active by default.
    is_active = models.BooleanField(
        default=True,
    )

    # Automatically record when the student fee record is created.
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    # Automatically update the timestamp whenever the record is saved.
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    # Define database-level rules for student fee records.
    class Meta:

        # Prevent the same student from having more than one StudentFee
        # record for the same academic year.
        # This uniqueness rule applies even if a record is inactive.
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "student",
                    "academic_year",
                ],
                name="unique_student_fee_per_year",
            )
        ]

    # Calculate the total amount paid towards this student's fee.
    # @property allows us to access this calculation as amount_paid
    # instead of calling it as a regular method.
    @property
    def amount_paid(self):

        # Add together the amounts of all payments linked to this fee.
        # Sum("amount") calculates the total payment amount.
        # If no payments exist, return Decimal("0.00") instead of None.
        return self.payments.aggregate(
            total=Sum("amount")
        )["total"] or Decimal("0.00")

    # Calculate the outstanding balance on the student's fee.
    @property
    def balance(self):

        # Subtract the total amount paid from the amount due.
        # A positive result means money is still owed.
        # Zero means the fee has been fully paid.
        # A negative result means the recorded payments exceed the fee.
        return self.amount_due - self.amount_paid

    # Return a readable description of the student's fee record.
    def __str__(self):
        return (
            f"{self.student} - "
            f"{self.academic_year} - "
            f"K{self.amount_due}"
        )


# ============================================================
# PAYMENT MODEL
# Records each individual payment made towards a student's fee.
# Multiple payments can be linked to one StudentFee record.
# ============================================================
class Payment(models.Model):

    # Define the payment methods accepted by the school.
    # Database values are stored in the first position of each tuple.
    # Human-readable labels are shown in forms and admin pages.
    PAYMENT_METHOD_CHOICES = [
        ("CASH", "Cash"),
        ("BANK", "Bank Transfer"),
        ("MOBILE", "Mobile Money"),
        ("CARD", "Card"),
    ]

    # Link this payment to the student's fee record.
    # One StudentFee record can have multiple Payment records.
    # PROTECT prevents deleting a student fee record with payments.
    # related_name allows access through student_fee.payments.
    student_fee = models.ForeignKey(
        StudentFee,
        on_delete=models.PROTECT,
        related_name="payments",
    )

    # Store the amount received in this individual transaction.
    # Decimal values are used to handle monetary amounts accurately.
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    # Store the date on which the payment was made.
    # DateField stores a date without a time component.
    payment_date = models.DateField()

    # Store the method used to pay the school fees.
    # The available methods are restricted by PAYMENT_METHOD_CHOICES.
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
    )

    # Store a unique receipt number for each payment.
    # unique=True prevents two payment records from using the same
    # receipt number.
    receipt_number = models.CharField(
        max_length=50,
        unique=True,
    )

    # Store an optional transaction reference.
    # This can contain a bank transaction ID or mobile money reference.
    # blank=True means this field can be left empty.
    reference = models.CharField(
        max_length=100,
        blank=True,
    )

    # Record the user who entered the payment into SchoolCore.
    # This links to the custom User model in the accounts app.
    # PROTECT prevents deleting a user who is referenced by payments.
    # related_name allows access through user.recorded_payments.
    recorded_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.PROTECT,
        related_name="recorded_payments",
    )

    # Store optional notes about the payment.
    # For example, this could explain a payment discrepancy.
    remarks = models.CharField(
        max_length=255,
        blank=True,
    )

    # Automatically record when this payment entry was created.
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    # Return a readable summary of the payment.
    # This can appear in Django admin and other object listings.
    def __str__(self):
        return (
            f"{self.receipt_number} - "
            f"{self.student_fee.student} - "
            f"K{self.amount}"
        )
