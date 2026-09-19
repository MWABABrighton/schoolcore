from django.db.models import Avg, Sum
from django.shortcuts import get_object_or_404, render

from students.models import Student


def get_grade(marks):
    if marks >= 80:
        return "A"
    elif marks >= 70:
        return "B"
    elif marks >= 60:
        return "C"
    elif marks >= 50:
        return "D"
    return "F"


def student_report_card(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    results = (
        student.results
        .select_related("subject", "examination")
        .order_by("subject__name")
    )

    for result in results:
        result.grade = get_grade(result.marks)

    summary = results.aggregate(
        total_marks=Sum("marks"),
        average_marks=Avg("marks"),
    )

    return render(
        request,
        "reports/student_report_card.html",
        {
            "student": student,
            "results": results,
            "total_marks": summary["total_marks"],
            "average_marks": summary["average_marks"],
        },
    )