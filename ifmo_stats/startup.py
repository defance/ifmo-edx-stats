
from django.conf.urls import include, url
from path import path
from xmodule.tabs import *
from xmodule import tabs
import edxmako

def patch_templates():
    # TODO Add template path to template look up path collection in settings
    template_path = path(__file__).dirname() / 'templates'
    edxmako.paths.add_lookup('main', template_path, prepend=True)


def _patch_variant_url(app_name, urls_module):
    app_urls = __import__('%s.urls' % (app_name,), fromlist=['urlpatterns'])
    app_urls.urlpatterns.insert(0, url(r'', include(urls_module)))


def patch_tabs():
    tabs.StatsTab = StatsTab
    tabs.CourseTabList.iterate_displayable = patch_iterate_displayable(tabs.CourseTabList.iterate_displayable)


def patch_urls():
    try:
        _patch_variant_url('lms', 'ifmo_stats.urls')
    except Exception:
        pass


class StatsTab(StaffTab):
    type = 'stats'
    is_movable = False
    def __init__(self, tab_dict=None):  # pylint: disable=unused-argument
        super(StatsTab, self).__init__(
            name=('Stats'),
            tab_id=self.type,
            link_func=link_reverse_func('stats'),
        )


def patch_iterate_displayable(func):
    @staticmethod
    def patch(
            course,
            settings,
            is_user_authenticated=True,
            is_user_staff=True,
            is_user_enrolled=False
    ):
        for el in func(course, settings, is_user_authenticated, is_user_staff, is_user_enrolled):
            yield el
        ifmo_stats = StatsTab()
        if ifmo_stats.can_display(course, settings, is_user_authenticated, is_user_staff, is_user_enrolled):
            yield ifmo_stats
    return patch


def run():
    patch_templates()
    patch_urls()
    patch_tabs()