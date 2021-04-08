"""

XBlock for presenting the user with a wizard for generating learning objectives
associated with a unit.

Learning objectives are a specialized statement describing what learners are
expected 'get' out of a lesson. Linking this statement to ABET outcomes
based on Bloom's taxonomy.


Author : Cary Rivet

"""

import datetime, json, urllib.request, urllib.error, urllib.parse, logging

from xblock.core import XBlock
from xblock.fields import (
        Scope,
        Integer,
        List,
        String,
        Boolean,
        Dict,
        Reference, # reference to another xblock
        ReferenceList, # list of references to other xblocks
    )




# including nested xblock container
#       source references for these:
#           https://github.com/edx/xblock-utils/blob/master/xblockutils/studio_editable.py
#
from xblockutils.settings import XBlockWithSettingsMixin
from xblockutils.studio_editable import (
    StudioEditableXBlockMixin,
    #StudioContainerXBlockMixin,
    StudioContainerWithNestedXBlocksMixin,
    NestedXBlockSpec,
    XBlockWithPreviewMixin,
)

from hl_text import hl_text_XBlock

from web_fragments.fragment import Fragment

# they do this in the mentoring block which implements this type of system
#   so i guess i have to as well right?
#       https://github.com/open-craft/problem-builder/blob/master/problem_builder/mentoring.py
#
# Make '_' a no-op so we can scrape strings
def _(text):
    return text


# initialize the log
log = logging.getLogger(__name__)

# initialize the resource loader
from xblockutils.resources import ResourceLoader
loader = ResourceLoader(__name__)


# origional implementation as just a text block (templated text block)
class HL_LearningActivity_XBlock(hl_text_XBlock):

    # modify path to the custom starter template for empty xblocks
    #empty_template = 'templates/initial_learning_activity_template.html'

    display_name = String(
        display_name="Learning Activity",
        help="This name appears in the horizontal navigation at the top of the page",
        scope=Scope.settings,
        default="Learning Activity (Template)"
    )

    def get_empty_template(self, context={}):
        return loader.render_django_template('templates/initial_learning_activity_template.html', context)

    def studio_view(self, context):

        fragment = super(HL_LearningActivity_XBlock, self).studio_view(context)

        # fragment.add_css(loader.load_unicode('static/css/learning_activity_styling.css'))
        # fragment.add_javascript(loader.load_unicode('static/js/learning_activity_script.js'))
        # fragment.initialize_js('Learning_Activity_Studio')

        return fragment

    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("HL Learning Activity text XBlock",
             """<hl_learning_activities_text/>
             """),

        ]


