"""

XBlock for presenting the user with a wizard for generating learning objectives
associated with a unit.

Learning objectives are a specialized statement describing what learners are
expected 'get' out of a lesson. Linking this statement to ABET outcomes
based on Bloom's taxonomy.


Author : Cary Rivet

"""

import urllib, datetime, json, urllib2, logging
from .utils import render_template, load_resource, resource_string
from django.template import Context, Template

# imports for content indexing support
import re
from xmodule.util.misc import escape_html_characters

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
from xblockutils.studio_editable import (
    StudioEditableXBlockMixin,
    #StudioContainerXBlockMixin,
    StudioContainerWithNestedXBlocksMixin,
    NestedXBlockSpec,
)

from web_fragments.fragment import Fragment

# they do this in the mentoring block which implements this type of system
#   so i guess i have to as well right?
#       https://github.com/open-craft/problem-builder/blob/master/problem_builder/mentoring.py
#
# Make '_' a no-op so we can scrape strings
def _(text):
    return text


log = logging.getLogger(__name__)

# import the hydrolearn custom text xblock
# from hl_text import hl_text_XBlock

class HL_LearningActivity_XBlock(StudioContainerWithNestedXBlocksMixin, StudioEditableXBlockMixin, XBlock):

    # modify path to the custom starter template for empty xblocks
    #empty_template = 'templates/initial_learning_activity_template.html'
    has_children = True

    # CHILD_PREVIEW_TEMPLATE = "templates/default_preview_view.html"

    display_name = String(
        display_name="Learning Activity",
        help="This name appears in the horizontal navigation at the top of the page",
        scope=Scope.settings,
        default="Learning Activity"
    )

    editable_fields = ('display_name')

    @property
    def allowed_nested_blocks(self):  # pylint: disable=no-self-use
        """
        Returns a list of allowed nested XBlocks. Each item can be either
        * An XBlock class
        * A NestedXBlockSpec
        If XBlock class is used it is assumed that this XBlock is enabled and allows multiple instances.
        NestedXBlockSpec allows explicitly setting disabled/enabled state, disabled reason (if any) and single/multiple
        instances
        """

        """
            TODO: something about this needs to be fixed, figure out what it is

        """

        additional_blocks = []

        try:
            from .child_blocks import la_intro
            additional_blocks.append(NestedXBlockSpec(
                    la_intro,
                    single_instance=True,
                    disabled=False,
                    category='la_intro',
                    label=_(u"Introduction")
                ))
        except ImportError:
            # LOG.warning('Failed to Load HL Text block.')
            log.warning("Failed to import 'Introduction' activity component.")
            pass

        try:
            from .child_blocks import la_step
            additional_blocks.append(NestedXBlockSpec(
                    la_step,
                    single_instance=False,
                    disabled=False,
                    category='la_step',
                    label=_(u"Activity Step")
                ))
        except ImportError:
            # LOG.warning('Failed to Load HL Text block.')
            log.warning("Failed to import 'Step' activity component.")
            pass



        try:
            from hl_text import hl_text_XBlock
            additional_blocks.append(NestedXBlockSpec(
                    hl_text_XBlock,
                    single_instance=False,
                    disabled=False,
                    category='hl_text',
                    label=_(u"Text")
                ))
        except ImportError:
            # LOG.warning('Failed to Load HL Text block.')
            log.warning("Failed to import 'Introduction' activity component.")
            pass


        return additional_blocks

    def get_empty_template(self, context={}):
        return render_template('templates/initial_learning_activity_template.html', context)

    def studio_view(self, context):

        fragment = Fragment()

        fragment.add_content(render_template('templates/hl_learning_activity-cms.html', context))

        fragment.add_css(load_resource('static/css/hl_learning_activity-cms.css'))
        fragment.add_javascript(load_resource('static/js/hl_learning_activity-cms.js'))
        fragment.initialize_js('Learning_Activity_Studio')

        return fragment

    def student_view(self, context):

        fragment = Fragment()

        fragment.add_css(load_resource('static/css/hl_learning_activity-lms.css'))
        fragment.add_content(render_template('templates/hl_learning_activity-lms.html', context))
        fragment.add_javascript(load_resource('static/js/hl_learning_activity-lms.js'))
        fragment.initialize_js('Learning_Activity')

        # iterate all children
        # for usage_id in self.get_children():
        #     self.get_child(usage_id)
        #     self.runtime.render_children()

        # to render a specific child


        # to render all children
        # self.runtime.render_children()

        # to render correctly apparently need to add fragment resources
        # somehow using these methods/properties

        # fragment.content
        # fragment.add_frag_resources()
        # fragment.add_frags_resources() # for all children

        return fragment


    # def author_edit_view(self, context):
    #     """
    #     Child blocks can override this to control the view shown to authors in Studio when
    #     editing this block's children.
    #     """
    #     fragment = Fragment()
    #     self.render_children(context, fragment, can_reorder=True, can_add=True)
    #     return fragment
    #
    # def author_preview_view(self, context):
    #     """
    #     Child blocks can override this to add a custom preview shown to authors in Studio when
    #     not editing this block's children.
    #     """
    #     return self.student_view(context)




# origional implementation as just a text block
# class HL_LearningActivity_XBlock(hl_text_XBlock):
#
#     # modify path to the custom starter template for empty xblocks
#     #empty_template = 'templates/initial_learning_activity_template.html'
#
#     display_name = String(
#         display_name="Learning Activity",
#         help="This name appears in the horizontal navigation at the top of the page",
#         scope=Scope.settings,
#         default="Learning Activity"
#     )
#
#     def get_empty_template(self, context={}):
#         return render_template('templates/initial_learning_activity_template.html', context)
#
#     def studio_view(self, context):
#
#         fragment = super(HL_LearningActivity_XBlock, self).studio_view(context)
#
#         fragment.add_css(load_resource('static/css/learning_activity_styling.css'))
#         fragment.add_javascript(load_resource('static/js/learning_activity_script.js'))
#         fragment.initialize_js('Learning_Activity_Studio')
#
#         return fragment
#
#     def student_view(self, context):
#
#         fragment = super(HL_LearningActivity_XBlock, self).student_view(context)
#
#
#         return fragment
