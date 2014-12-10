from django.conf.urls import patterns, include, url
from django.conf import settings

urlpatterns = patterns('',
    url(r'^courses/{}/stats/grade/ajax$'.format(settings.COURSE_ID_PATTERN), 'ifmo_stats.views.save_grade', name="statsAjax"),
    url(r'^courses/{}/stats/grade$'.format(settings.COURSE_ID_PATTERN), 'ifmo_stats.views.grade', name="statsGrade"),
    url(r'^courses/{}/stats$'.format(settings.COURSE_ID_PATTERN), 'ifmo_stats.views.stats', name="stats"),
    url(r'^courses/{}/stats/grade/csv$'.format(settings.COURSE_ID_PATTERN), 'ifmo_stats.views.csv_out', name="csvGraded"),
)
