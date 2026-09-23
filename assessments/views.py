from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import role_required
from students.models import Enrolment

from .forms import ExaminationForm, ResultForm
from .models import Examination, Result


@login_required
def assessment_home(request):

    return render(
        request,
        "assessments/home.html",
    )


@role_required("DIRECTOR", "HEAD")
def create_examination(request):

    if request.method == "POST":

        form = ExaminationForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect(
                "assessment_home"
            )

    else:

        form = ExaminationForm()

    return render(
        request,
        "assessments/examination_form.html",
        {
            "form": form,
        },
    )


@role_required("TEACHER")
def teacher_examinations(request):

    teacher = getattr(
        request.user,
        "teacher_profile",
        None,
    )

    if teacher is None:

        return render(
            request,
            "assessments/access_denied.html",
            {
                "message": (
                    "Your user account is not linked "
                    "to a teacher profile."
                ),
            },
            status=403,
        )

    assignments = teacher.teaching_assignments.filter(
        is_active=True,
    )

    examinations = (
        Examination.objects
        .filter(
            is_active=True,
        )
        .select_related(
            "academic_year",
            "class_section",
            "subject",
        )
        .order_by(
            "academic_year__year",
            "term",
            "class_section__name",
            "subject__name",
        )
    )

    allowed_examinations = []

    for examination in examinations:

        assigned = assignments.filter(
            subject=examination.subject,
            section=examination.class_section,
            academic_year=examination.academic_year,
        ).exists()

        if assigned:

            allowed_examinations.append(
                examination
            )

    return render(
        request,
        "assessments/teacher_examinations.html",
        {
            "examinations": allowed_examinations,
        },
    )


@role_required("TEACHER")
def enter_marks(request, examination_id):

    examination = get_object_or_404(
        Examination.objects.select_related(
            "academic_year",
            "class_section",
            "subject",
        ),
        id=examination_id,
        is_active=True,
    )

    teacher = getattr(
        request.user,
        "teacher_profile",
        None,
    )

    if teacher is None:

        return render(
            request,
            "assessments/access_denied.html",
            {
                "message": (
                    "Your user account is not linked "
                    "to a teacher profile."
                ),
            },
            status=403,
        )

    assignment_exists = teacher.teaching_assignments.filter(
        subject=examination.subject,
        section=examination.class_section,
        academic_year=examination.academic_year,
        is_active=True,
    ).exists()

    if not assignment_exists:

        return render(
            request,
            "assessments/access_denied.html",
            {
                "message": (
                    "You are not assigned to teach "
                    "this subject and class."
                ),
            },
            status=403,
        )

    enrolments = (
        Enrolment.objects
        .filter(
            section=examination.class_section,
            academic_year=examination.academic_year,
            is_active=True,
            student__is_active=True,
        )
        .select_related("student")
        .order_by(
            "student__last_name",
            "student__first_name",
        )
    )

    existing_results = {
        result.student_id: result
        for result in Result.objects.filter(
            examination=examination,
        )
    }

    if request.method == "POST":

        for enrolment in enrolments:

            marks_value = request.POST.get(
                f"marks_{enrolment.student.id}",
                "",
            ).strip()

            remarks_value = request.POST.get(
                f"remarks_{enrolment.student.id}",
                "",
            ).strip()

            if marks_value == "":
                continue

            form = ResultForm(
                {
                    "marks": marks_value,
                    "remarks": remarks_value,
                }
            )

            if form.is_valid():

                Result.objects.update_or_create(
                    student=enrolment.student,
                    examination=examination,
                    defaults={
                        "marks": form.cleaned_data["marks"],
                        "remarks": form.cleaned_data["remarks"],
                        "recorded_by": request.user,
                    },
                )

        return redirect(
            "enter_marks",
            examination_id=examination.id,
        )

    return render(
        request,
        "assessments/enter_marks.html",
        {
            "examination": examination,
            "enrolments": enrolments,
            "existing_results": existing_results,
        },
    )
    