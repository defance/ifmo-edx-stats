
from django.conf.urls import include, url
from path import path
import django.contrib.staticfiles
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
    tabs.CourseTab.from_json = from_json
    tabs.CourseTab.iterate_displayable = iterate_displayable

class StatsTab(CourseTab):
    type = 'stats'
    is_movable = False
    def __init__(self, tab_dict=None):  # pylint: disable=unused-argument
        super(StatsTab, self).__init__(
            name=('Stats'),
            tab_id=self.type,
            link_func=link_reverse_func('stats'),
        )


def patch_urls():
    try:
        _patch_variant_url('lms', 'ifmo_stats.urls')
    except Exception:
        pass





def from_json(tab_dict):
        """
        Deserializes a CourseTab from a json-like representation.
        The subclass that is instantiated is determined by the value of the 'type' key in the
        given dict-type tab. The given dict-type tab is validated before instantiating the CourseTab object.
        Args:
            tab: a dictionary with keys for the properties of the tab.
        Raises:
            InvalidTabsException if the given tab doesn't have the right keys.
        """
        sub_class_types = {
            'courseware': CoursewareTab,
            'course_info': CourseInfoTab,
            'wiki': WikiTab,
            'discussion': DiscussionTab,
            'external_discussion': ExternalDiscussionTab,
            'external_link': ExternalLinkTab,
            'textbooks': TextbookTabs,
            'pdf_textbooks': PDFTextbookTabs,
            'html_textbooks': HtmlTextbookTabs,
            'progress': ProgressTab,
            'static_tab': StaticTab,
            'peer_grading': PeerGradingTab,
            'staff_grading': StaffGradingTab,
            'open_ended': OpenEndedGradingTab,
            'notes': NotesTab,
            'syllabus': SyllabusTab,
            'instructor': InstructorTab,  # not persisted
            'stats': StatsTab,
        }

        tab_type = tab_dict.get('type')
        if tab_type not in sub_class_types:
            raise InvalidTabsException(
                'Unknown tab type {0}. Known types: {1}'.format(tab_type, sub_class_types)
            )

        tab_class = sub_class_types[tab_dict['type']]
        tab_class.validate(tab_dict)
        return tab_class(tab_dict=tab_dict)

def iterate_displayable(
            course,
            settings,
            is_user_authenticated=True,
            is_user_staff=True,
            is_user_enrolled=False
    ):
        """
        Generator method for iterating through all tabs that can be displayed for the given course and
        the given user with the provided access settings.
        """
        for tab in course.tabs:
            if tab.can_display(
                    course, settings, is_user_authenticated, is_user_staff, is_user_enrolled
            ) and (not tab.is_hideable or not tab.is_hidden):
                if tab.is_collection:
                    for item in tab.items(course):
                        yield item
                else:
                    yield tab
        instructor_tab = InstructorTab()
        if instructor_tab.can_display(course, settings, is_user_authenticated, is_user_staff, is_user_enrolled):
            yield instructor_tab
        ifmo_stats = StatsTab()
        yield ifmo_stats

def run():
    patch_templates()
    patch_urls()
    patch_tabs()