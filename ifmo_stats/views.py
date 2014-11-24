from edxmako.shortcuts import render_to_response
from django_future.csrf import ensure_csrf_cookie
from courseware.views import verify_course_id
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from opaque_keys.edx.locations import SlashSeparatedCourseKey
from courseware.courses import get_course_by_id


@login_required
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
@ensure_csrf_cookie
@verify_course_id
def courses(request, course_id):

    course_key = SlashSeparatedCourseKey.from_deprecated_string(course_id)
    course = get_course_by_id(course_key, depth=None)
    context = {
        'request': request,
       'course': course,
    }
    return render_to_response("test.html", context)
