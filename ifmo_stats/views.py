from edxmako.shortcuts import render_to_response
from django.views.decorators.cache import cache_control
from opaque_keys.edx.locations import SlashSeparatedCourseKey
from instructor.views.api import require_level
from courseware.courses import get_course_with_access
from django.contrib.auth.models import User
from instructor.offline_gradecalc import student_grades
from django.http import HttpResponse
from models import Grading
from datetime import date
from xmodule.graders import AssignmentFormatGrader
from south.models import MigrationHistory

@cache_control(no_cache=True, no_store=True, must_revalidate=True)
@require_level('staff')
def grade(request, course_id):
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

    grading_filter = Grading.objects.filter(
        course_id=course_id
    )

    grading = [
        {
            'problem_number': grade.problem_number,
            'deadline': grade.deadline,
            'min_grade': grade.min_grade
        }
        for grade in grading_filter
    ]
    # possible extension: implement pagination to show to large courses
<<<<<<< HEAD
    """grading_context = course.grading_context
    for section_format, sections in grading_context['graded_sections'].iteritems():
        for section in sections:
            print section['section_descriptor'].display_name_with_default

    print course.grader.sections[0][0].short_label"""
=======
    grading_context = course.grading_context
    for section_format, sections in grading_context['graded_sections'].iteritems():
        for section in sections:
            print [descriptor.location for descriptor in section['xmoduledescriptors']]

    print course.grader.sections[0][0].short_label
>>>>>>> added grading and stats
    student_info = [
        {
            'username': enrolled_students[0].username,
            'id': enrolled_students[0].id,
            'email': enrolled_students[0].email,
            'grade_summary': student_grades(enrolled_students[0], request, course),
            'realname': enrolled_students[0].profile.name,
        }
        #for student in enrolled_students
    ]
    print student_info[0]['grade_summary']['percent']
    return render_to_response('easyGradebook.html', {
        'url': request.path,
        'students': student_info,
        'course': course,
        'course_id': course_key,
<<<<<<< HEAD
        'course_raw_id':course_id,
=======
>>>>>>> added grading and stats
        'grading': grading,
        # Checked above
        'staff_access': True,
        'ordered_grades': sorted(course.grade_cutoffs.items(), key=lambda i: i[1], reverse=True),
    })


def save_grade(request, course_id):
    grade_data = Grading()
    try:
        grade_data = Grading.objects.get(
            course_id = course_id,
            problem_number = (int(request.POST.get('tabindex'))+1)//2)
    except Exception:
        grade_data = Grading(
            course_id = course_id,
            problem_number = (int(request.POST.get('tabindex'))+1)//2)

    if not int(request.POST.get('tabindex'))%2:
        value = request.POST.get('value').split("/")
        grade_data.deadline = date(day=int(value[0]), month=int(value[1]), year=int(value[2]))
    else:
        grade_data.min_grade = float(request.POST.get('value'))/100
    grade_data.save()
    return HttpResponse("???")

@cache_control(no_cache=True, no_store=True, must_revalidate=True)
@require_level('staff')
def stats(request, course_id):
    course_key = SlashSeparatedCourseKey.from_deprecated_string(course_id)
    course = get_course_with_access(request.user, 'staff', course_key, depth=None)
    enrolled_students = User.objects.filter(
        courseenrollment__course_id=course_key,
        courseenrollment__is_active=1
    ).order_by('username').select_related("profile")
    grading_filter = Grading.objects.filter(
        course_id=course_id
    )
    grading = {}

    for el in grading_filter:
        grading[el.problem_number-1] = el.min_grade
    """
    all_stats
    [0] - Total
    [1] - Tried
    [2] - OverZero
    [3] - OverMin
    [4] - Max
    [5] - Zero
    """

    all_stats = []
    for section in student_grades(enrolled_students[0], request, course)['section_breakdown']:
        if(section['label'][-3:] != 'Avg'):
            scores = []
            for i in range(0, 6):
                scores.append(0)
            all_stats.append([section['label'], scores])

    for student in enrolled_students:
        j = 0
        for section in student_grades(student, request, course)['section_breakdown']:
            if(section['label'][-3:] != 'Avg'):
                if(section['percent'] > 0):
                    all_stats[j][1][2] += 1
                if(grading.get(j) and section['percent'] >= grading[j]):
                    all_stats[j][1][3] += 1
                if(section['percent'] == 1.0):
                    all_stats[j][1][4] += 1
                if(section['percent'] == 0):
                    all_stats[j][1][5] += 1
                j += 1

    return render_to_response('stats.html', {
        'url': request.path,
        'course': course,
        'course_id': course_key,
        'all_stats': all_stats,
        'staff_access': True,
    })
