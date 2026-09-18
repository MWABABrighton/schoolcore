from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Examination(models.Model):
    TERM_CHOICES = [
        ("TERM1", "Term 1"),
        ("TERM2", "Term 2"),
        ("TERM3", "Term 3"),
    ]

    name = models.CharField(max_length=100)

    academic_year = models.ForeignKey(
        "academics.AcademicYear",
        on_delete=models.PROTECT,
        related_name="examinations",
    )

    term = models.CharField(
        max_length=10,
        choices=TERM_CHOICES,
    )

    start_date = models.DateField()
    end_date = models.DateField()

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.academic_year} - {self.get_term_display()}"


class Result(models.Model):
    student = models.ForeignKey(
        "students.Student",
        on_delete=models.PROTECT,
        related_name="results",
    )

    examination = models.ForeignKey(
        Examination,
        on_delete=models.PROTECT,
        related_name="results",
    )

    subject = models.ForeignKey(
        "academics.Subject",
        on_delete=models.PROTECT,
        related_name="results",
    )

    marks = models.DecimalField(
    max_digits=5,
    decimal_places=2,
    validators=[
        MinValueValidator(0),
        MaxValueValidator(100),
    ],
)

    remarks = models.CharField(
        max_length=255,
        blank=True,
    )

    recorded_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.PROTECT,
        related_name="recorded_results",
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
                fields=["student", "examination", "subject"],
                name="unique_student_result_per_subject",
            )
        ]

    def __str__(self):
        return (
            f"{self.student} - "
            f"{self.examination} - "
            f"{self.subject} - "
            f"{self.marks}"
        )