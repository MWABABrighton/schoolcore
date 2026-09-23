from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from academics.models import SchoolClass, Section
from .forms import StudentForm
from .models import Enrolment, Student


def student_list(request):

    search_query = request.GET.get(
        "search",
        "",
    ).strip()

    class_id = request.GET.get(
        "class_id",
        "",
    )

    section_id = request.GET.get(
        "section_id",
        "",
    )

    students = Student.objects.filter(
        is_active=True
    )

    # Search
    if search_query:

        search_terms = search_query.split()

        for term in search_terms:

            students = students.filter(
                Q(student_number__icontains=term)
                | Q(first_name__icontains=term)
                | Q(middle_name__icontains=term)
                | Q(last_name__icontains=term)
            )

    # Filter by class
    if class_id:

        students = students.filter(
            enrolments__section__school_class_id=class_id,
            enrolments__is_active=True,
        )

    # Filter by section
    if section_id:

        students = students.filter(
            enrolments__section_id=section_id,
            enrolments__is_active=True,
        )

    students = students.order_by(
        "last_name",
        "first_name",
    ).distinct()

    # Pagination
    paginator = Paginator(
        students,
        20,
    )

    page_number = request.GET.get(
        "page"
    )

    page_obj = paginator.get_page(
        page_number
    )

    # Classes for filter dropdown
    school_classes = SchoolClass.objects.all().order_by(
        "name"
    )

    # Sections for filter dropdown
    sections = Section.objects.select_related(
        "school_class"
    ).order_by(
        "school_class__name",
        "name",
    )

    return render(
        request,
        "students/student_list.html",
        {
            "students": page_obj,
            "page_obj": page_obj,
            "search_query": search_query,
            "school_classes": school_classes,
            "sections": sections,
            "selected_class": class_id,
            "selected_section": section_id,
        },
    )


def student_create(request):

    if request.method == "POST":

        form = StudentForm(request.POST)

        if form.is_valid():

            student = form.save()

            Enrolment.objects.create(
                student=student,
                academic_year=form.cleaned_data["academic_year"],
                section=form.cleaned_data["section"],
            )

            return redirect(
                "student_detail",
                student_id=student.id,
            )

    else:

        form = StudentForm()

    return render(
        request,
        "students/student_form.html",
        {
            "form": form,
        },
    )


def student_detail(request, student_id):

    student = get_object_or_404(
        Student,
        id=student_id,
    )

    enrolments = student.enrolments.select_related(
        "academic_year",
        "section",
        "section__school_class",
    ).order_by(
        "-academic_year__year"
    )

    return render(
        request,
        "students/student_detail.html",
        {
            "student": student,
            "enrolments": enrolments,
        },
    )