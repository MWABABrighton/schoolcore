from accounts.decorators import role_required
from django.db.models import Avg, Sum
from django.shortcuts import get_object_or_404, render

from students.models import Enrolment, Student
from teachers.models import ClassTeacherAssignment


@role_required("DIRECTOR", "HEAD", "TEACHER")
def reports_home(request):

    return render(
        request,
        "reports/home.html",
    )


def get_grade(marks):

    if marks >= 80:

        return "Distinction"

    elif marks >= 60:

        return "Merit"

    elif marks >= 50:

        return "Credit"

    return "Fail"


@role_required("DIRECTOR", "HEAD", "TEACHER")
def student_report_card(request, student_id):

    student = get_object_or_404(
        Student,
        id=student_id,
    )

    term = request.GET.get(
        "term",
        "",
    )

    assignment_id = request.GET.get(
        "assignment",
        "",
    )

    assignment = None

    if assignment_id:

        assignment = get_object_or_404(
            ClassTeacherAssignment.objects.select_related(
                "section",
                "section__school_class",
                "academic_year",
            ),
            id=assignment_id,
            is_active=True,
        )

        if request.user.role == "TEACHER":

            if assignment.teacher != request.user.teacher_profile:

                return render(
                    request,
                    "reports/access_denied.html",
                    {
                        "message": (
                            "You do not have permission "
                            "to access this class report."
                        ),
                    },
                    status=403,
                )

    elif request.user.role == "TEACHER":

        return render(
            request,
            "reports/access_denied.html",
            {
                "message": (
                    "Teachers must access student reports "
                    "through their assigned class."
                ),
            },
            status=403,
        )

    results = (
        student.results
        .select_related(
            "examination",
            "examination__academic_year",
            "examination__class_section",
            "examination__subject",
        )
    )

    if assignment:

        results = results.filter(
            examination__academic_year=assignment.academic_year,
            examination__class_section=assignment.section,
        )

        if request.user.role == "TEACHER":

            student_is_enrolled = Enrolment.objects.filter(
                student=student,
                section=assignment.section,
                academic_year=assignment.academic_year,
                is_active=True,
            ).exists()

            if not student_is_enrolled:

                return render(
                    request,
                    "reports/access_denied.html",
                    {
                        "message": (
                            "This student is not enrolled "
                            "in your assigned class."
                        ),
                    },
                    status=403,
                )

    if term:

        results = results.filter(
            examination__term=term,
        )

    results = results.order_by(
        "examination__subject__name",
    )

    for result in results:

        result.grade = get_grade(
            result.marks
        )

    summary = results.aggregate(
        total_marks=Sum("marks"),
        average_marks=Avg("marks"),
    )

    report_academic_year = None
    report_term = None
    report_class = None

    if assignment:

        report_academic_year = (
            assignment.academic_year
        )

        report_class = (
            assignment.section
        )

    elif results.exists():

        first_result = results.first()

        report_academic_year = (
            first_result.examination.academic_year
        )

        report_class = (
            first_result.examination.class_section
        )

    if term == "TERM1":

        report_term = "Term 1"

    elif term == "TERM2":

        report_term = "Term 2"

    elif term == "TERM3":

        report_term = "Term 3"

    elif results.exists():

        report_term = (
            results.first()
            .examination
            .get_term_display()
        )

    return render(
        request,
        "reports/student_report_card.html",
        {
            "student": student,
            "results": results,
            "total_marks": summary["total_marks"],
            "average_marks": summary["average_marks"],
            "report_academic_year": report_academic_year,
            "report_term": report_term,
            "report_class": report_class,
        },
    )


@role_required("DIRECTOR", "HEAD", "TEACHER")
def my_class_reports(request):

    if request.user.role in ["DIRECTOR", "HEAD"]:

        class_assignments = (
            ClassTeacherAssignment.objects
            .filter(
                is_active=True,
            )
            .select_related(
                "section",
                "section__school_class",
                "academic_year",
                "teacher",
            )
            .order_by(
                "-academic_year__year",
                "section__school_class__name",
                "section__name",
            )
        )

    else:

        teacher = getattr(
            request.user,
            "teacher_profile",
            None,
        )

        if teacher is None:

            return render(
                request,
                "reports/access_denied.html",
                {
                    "message": (
                        "Your user account is not linked "
                        "to a teacher profile."
                    ),
                },
                status=403,
            )

        class_assignments = (
            teacher.class_teacher_assignments
            .filter(
                is_active=True,
            )
            .select_related(
                "section",
                "section__school_class",
                "academic_year",
                "teacher",
            )
            .order_by(
                "-academic_year__year",
                "section__school_class__name",
                "section__name",
            )
        )

    return render(
        request,
        "reports/my_class_reports.html",
        {
            "class_assignments": class_assignments,
        },
    )


@role_required("DIRECTOR", "HEAD", "TEACHER")
def class_report_cards(request, assignment_id):

    teacher = getattr(
        request.user,
        "teacher_profile",
        None,
    )

    assignment = get_object_or_404(
        ClassTeacherAssignment.objects.select_related(
            "section",
            "section__school_class",
            "academic_year",
            "teacher",
        ),
        id=assignment_id,
        is_active=True,
    )

    if request.user.role == "TEACHER":

        if assignment.teacher != teacher:

            return render(
                request,
                "reports/access_denied.html",
                {
                    "message": (
                        "You do not have permission "
                        "to access this class."
                    ),
                },
                status=403,
            )

    term = request.GET.get(
        "term",
        "",
    )

    enrolments = (
        Enrolment.objects
        .filter(
            section=assignment.section,
            academic_year=assignment.academic_year,
            is_active=True,
            student__is_active=True,
        )
        .select_related(
            "student",
        )
        .order_by(
            "student__last_name",
            "student__first_name",
        )
    )

    return render(
        request,
        "reports/class_report_cards.html",
        {
            "assignment": assignment,
            "enrolments": enrolments,
            "selected_term": term,
        },
    )


@role_required("DIRECTOR", "HEAD", "TEACHER")
def print_class_report_cards(request, assignment_id):

    teacher = getattr(
        request.user,
        "teacher_profile",
        None,
    )

    assignment = get_object_or_404(
        ClassTeacherAssignment.objects.select_related(
            "section",
            "section__school_class",
            "academic_year",
            "teacher",
        ),
        id=assignment_id,
        is_active=True,
    )

    if request.user.role == "TEACHER":

        if assignment.teacher != teacher:

            return render(
                request,
                "reports/access_denied.html",
                {
                    "message": (
                        "You do not have permission "
                        "to print this class's reports."
                    ),
                },
                status=403,
            )

    term = request.GET.get(
        "term",
        "",
    )

    enrolments = (
        Enrolment.objects
        .filter(
            section=assignment.section,
            academic_year=assignment.academic_year,
            is_active=True,
            student__is_active=True,
        )
        .select_related(
            "student",
        )
        .order_by(
            "student__last_name",
            "student__first_name",
        )
    )

    report_cards = []

    for enrolment in enrolments:

        student = enrolment.student

        results = (
            student.results
            .select_related(
                "examination",
                "examination__academic_year",
                "examination__class_section",
                "examination__subject",
            )
            .filter(
                examination__academic_year=assignment.academic_year,
                examination__class_section=assignment.section,
            )
        )

        if term:

            results = results.filter(
                examination__term=term,
            )

        results = results.order_by(
            "examination__subject__name",
        )

        for result in results:

            result.grade = get_grade(
                result.marks
            )

        summary = results.aggregate(
            total_marks=Sum("marks"),
            average_marks=Avg("marks"),
        )

        if term == "TERM1":

            report_term = "Term 1"

        elif term == "TERM2":

            report_term = "Term 2"

        elif term == "TERM3":

            report_term = "Term 3"

        else:

            report_term = None

        report_cards.append(
            {
                "student": student,
                "results": results,
                "total_marks": summary["total_marks"],
                "average_marks": summary["average_marks"],
                "report_academic_year": assignment.academic_year,
                "report_term": report_term,
                "report_class": assignment.section,
            }
        )

    return render(
        request,
        "reports/print_class_report_cards.html",
        {
            "assignment": assignment,
            "report_cards": report_cards,
        },
    )