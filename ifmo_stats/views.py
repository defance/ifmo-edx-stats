from edxmako.shortcuts import render_to_response
from django.views.decorators.cache import cache_control
from opaque_keys.edx.locations import SlashSeparatedCourseKey
from instructor.views.api import require_level
from courseware.courses import get_course_with_access
from django.contrib.auth.models import User
from instructor.offline_gradecalc import student_grades

@cache_control(no_cache=True, no_store=True, must_revalidate=True)
@require_level('staff')
def gradebook(request, course_id):
    """
    Show the gradebook for this course:
    - Only shown for courses with enrollment < settings.FEATURES.get("MAX_ENROLLMENT_INSTR_BUTTONS")
    - Only displayed to course staff
    """
    course_key = SlashSeparatedCourseKey.from_deprecated_string(course_id)
    course = get_course_with_access(request.user, 'staff', course_key, depth=None)

    enrolled_students = User.objects.filter(
        courseenrollment__course_id=course_key,
        courseenrollment__is_active=1
    ).order_by('username').select_related("profile")

    # possible extension: implement pagination to show to large courses

    student_info = [
        {
            'username': student.username,
            'id': student.id,
            'email': student.email,
            'grade_summary': student_grades(student, request, course),
            'realname': student.profile.name,
        }
        for student in enrolled_students
    ]

    return render_to_response('ifmoGradebook.html', {
        'students': student_info,
        'course': course,
        'course_id': course_key,
        # Checked above
        'staff_access': True,
        'ordered_grades': sorted(course.grade_cutoffs.items(), key=lambda i: i[1], reverse=True),
    })
