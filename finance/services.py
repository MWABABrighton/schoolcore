from .models import FeeStructure, StudentFee


def allocate_fees_for_enrolment(enrolment):
    """
    Create the student's fee account for the academic year
    using the applicable tuition fee structure.
    """

    fee_structure = FeeStructure.objects.filter(
        academic_year=enrolment.academic_year,
        school_class=enrolment.section.school_class,
        fee_type="TUITION",
        is_active=True,
    ).first()

    if not fee_structure:
        return None

    student_fee, created = StudentFee.objects.get_or_create(
        student=enrolment.student,
        academic_year=enrolment.academic_year,
        defaults={
            "fee_structure": fee_structure,
            "amount_due": fee_structure.amount,
            "is_active": True,
        },
    )

    return student_fee