from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Examination(models.Model):

    TERM_CHOICES = [
        ("TERM1", "Term 1"),
        ("TERM2", "Term 2"),
        ("TERM3", "Term 3"),
    ]

    academic_year = models.ForeignKey(
        "academics.AcademicYear",
        on_delete=models.PROTECT,
        related_name="examinations",
    )

    term = models.CharField(
        max_length=10,
        choices=TERM_CHOICES,
    )

    class_section = models.ForeignKey(
        "academics.Section",
        on_delete=models.PROTECT,
        related_name="examinations",
        null=True,
    )

    subject = models.ForeignKey(
        "academics.Subject",
        on_delete=models.PROTECT,
        related_name="examinations",
        null=True,
    )

    exam_date = models.DateField(
        null=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    def __str__(self):
        return (
            f"{self.academic_year} - "
            f"{self.get_term_display()} - "
            f"{self.class_section} - "
            f"{self.subject}"
        )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "academic_year",
                    "term",
                    "class_section",
                    "subject",
                ],
                name="unique_end_of_term_exam",
            )
        ]


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
                fields=[
                    "student",
                    "examination",
                ],
                name="unique_student_result_per_exam",
            )
        ]

    def __str__(self):
        return (
            f"{self.student} - "
            f"{self.examination} - "
            f"{self.marks}"
        )