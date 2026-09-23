from django.db import models


class Teacher(models.Model):

    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
    ]

    user = models.OneToOneField(
        "accounts.User",
        on_delete=models.PROTECT,
        related_name="teacher_profile",
        null=True,
        blank=True,
    )

    employee_number = models.CharField(
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

    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
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

    employment_date = models.DateField(
        null=True,
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
            f"{self.employee_number} - "
            f"{self.first_name} "
            f"{self.last_name}"
        )


class TeachingAssignment(models.Model):

    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.PROTECT,
        related_name="teaching_assignments",
    )

    subject = models.ForeignKey(
        "academics.Subject",
        on_delete=models.PROTECT,
        related_name="teaching_assignments",
    )

    section = models.ForeignKey(
        "academics.Section",
        on_delete=models.PROTECT,
        related_name="teaching_assignments",
    )

    academic_year = models.ForeignKey(
        "academics.AcademicYear",
        on_delete=models.PROTECT,
        related_name="teaching_assignments",
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "teacher",
                    "subject",
                    "section",
                    "academic_year",
                ],
                name="unique_teaching_assignment",
            )
        ]

    def __str__(self):
        return (
            f"{self.teacher} - "
            f"{self.subject} - "
            f"{self.section} - "
            f"{self.academic_year}"
        )


class ClassTeacherAssignment(models.Model):

    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.PROTECT,
        related_name="class_teacher_assignments",
    )

    section = models.ForeignKey(
        "academics.Section",
        on_delete=models.PROTECT,
        related_name="class_teacher_assignments",
    )

    academic_year = models.ForeignKey(
        "academics.AcademicYear",
        on_delete=models.PROTECT,
        related_name="class_teacher_assignments",
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "section",
                    "academic_year",
                ],
                name="unique_class_teacher_per_section_year",
            )
        ]

    def __str__(self):
        return (
            f"{self.teacher} - "
            f"{self.section} - "
            f"{self.academic_year}"
        )