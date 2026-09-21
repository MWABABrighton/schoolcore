from django.db import models

from finance.services import allocate_fees_for_enrolment


class Student(models.Model):

    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
    ]

    student_number = models.CharField(
        max_length=20,
        unique=True,
    )

    first_name = models.CharField(
        max_length=100,
    )

    middle_name = models.CharField(
        max_length=100,
        blank=True,
    )

    last_name = models.CharField(
        max_length=100,
    )

    date_of_birth = models.DateField()

    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
    )

    phone_number = models.CharField(
        max_length=20,
        blank=True,
    )

    email = models.EmailField(
        blank=True,
    )

    address = models.TextField(
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
            f"{self.student_number} - "
            f"{self.first_name} "
            f"{self.last_name}"
        )


class Guardian(models.Model):

    RELATIONSHIP_CHOICES = [
        ("FATHER", "Father"),
        ("MOTHER", "Mother"),
        ("GUARDIAN", "Guardian"),
        ("OTHER", "Other"),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="guardians",
    )

    full_name = models.CharField(
        max_length=200,
    )

    relationship = models.CharField(
        max_length=20,
        choices=RELATIONSHIP_CHOICES,
    )

    phone_number = models.CharField(
        max_length=20,
    )

    email = models.EmailField(
        blank=True,
    )

    address = models.TextField(
        blank=True,
    )

    is_primary = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return (
            f"{self.full_name} - "
            f"{self.student}"
        )


class Enrolment(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="enrolments",
    )

    academic_year = models.ForeignKey(
        "academics.AcademicYear",
        on_delete=models.PROTECT,
        related_name="enrolments",
    )

    section = models.ForeignKey(
        "academics.Section",
        on_delete=models.PROTECT,
        related_name="enrolments",
    )

    enrolment_date = models.DateField(
        auto_now_add=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "student",
                    "academic_year",
                ],
                name="unique_student_per_academic_year",
            )
        ]

    def __str__(self):
        return (
            f"{self.student} - "
            f"{self.academic_year} - "
            f"{self.section}"
        )

    def save(self, *args, **kwargs):

        is_new = self.pk is None

        super().save(*args, **kwargs)

        if is_new:
            allocate_fees_for_enrolment(self)