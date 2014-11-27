from django.conf.urls import patterns, include, url
from django.conf import settings

urlpatterns = patterns('',
    url(r'^courses/{}/stats$'.format(settings.COURSE_ID_PATTERN), 'ifmo_stats.views.gradebook', name="stats"),
)
