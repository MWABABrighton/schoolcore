from django.db import models


class Attendance(models.Model):

    academic_year = models.ForeignKey(
        "academics.AcademicYear",
        on_delete=models.PROTECT,
        related_name="attendance_records",
    )

    section = models.ForeignKey(
        "academics.Section",
        on_delete=models.PROTECT,
        related_name="attendance_records",
    )

    date = models.DateField()

    recorded_by_name = models.CharField(
        max_length=150,
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
                    "academic_year",
                    "section",
                    "date",
                ],
                name="unique_attendance_per_class_date",
            )
        ]

        ordering = [
            "-date",
        ]

    def __str__(self):
        return (
            f"{self.section} - "
            f"{self.date}"
        )


class AttendanceEntry(models.Model):

    STATUS_CHOICES = [
        ("PRESENT", "Present"),
        ("ABSENT", "Absent"),
        ("PERMISSION", "Permission"),
        ("SICK", "Sick"),
    ]

    attendance = models.ForeignKey(
        Attendance,
        on_delete=models.CASCADE,
        related_name="entries",
    )

    student = models.ForeignKey(
        "students.Student",
        on_delete=models.PROTECT,
        related_name="attendance_entries",
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "attendance",
                    "student",
                ],
                name="unique_student_per_attendance",
            )
        ]

        ordering = [
            "student__last_name",
            "student__first_name",
        ]

    def __str__(self):
        return (
            f"{self.student} - "
            f"{self.attendance.date} - "
            f"{self.status}"
        )