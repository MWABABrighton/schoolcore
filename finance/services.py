from .models import FeeStructure, StudentFee


def allocate_fees_for_enrolment(enrolment):
    """
    Automatically allocate all active fee structures
    applicable to the student's class and academic year.
    """

    fee_structures = FeeStructure.objects.filter(
        academic_year=enrolment.academic_year,
        school_class=enrolment.section.school_class,
        is_active=True,
    )

    created_fees = []

    for fee_structure in fee_structures:

        student_fee, created = StudentFee.objects.get_or_create(
            student=enrolment.student,
            academic_year=enrolment.academic_year,
            fee_structure=fee_structure,
            defaults={
                "amount_due": fee_structure.amount,
                "is_active": True,
            },
        )

        if created:
            created_fees.append(student_fee)

    return created_fees