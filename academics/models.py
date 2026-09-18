from django.db import models


class AcademicYear(models.Model):
    year = models.PositiveIntegerField(unique=True)
    is_current = models.BooleanField(default=False)

    def __str__(self):
        return str(self.year)
class SchoolClass(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name

class Section(models.Model):
    school_class = models.ForeignKey(
        SchoolClass,
        on_delete=models.CASCADE,
        related_name="sections",
    )
    name = models.CharField(max_length=20)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["school_class", "name"],
                name="unique_section_per_class",
            )
        ]

    def __str__(self):
        return f"{self.school_class.name}{self.name}"
   
   
class Subject(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.code} - {self.name}"