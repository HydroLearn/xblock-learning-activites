"""

XBlock for presenting the user with a wizard for generating learning objectives
associated with a unit.

Learning objectives are a specialized statement describing what learners are
expected 'get' out of a lesson. Linking this statement to ABET outcomes
based on Bloom's taxonomy.


Author : Cary Rivet

"""

import urllib, datetime, json, urllib2
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
from xblockutils.studio_editable import StudioContainerXBlockMixin
from xblockutils.studio_editable import StudioEditableXBlockMixin

# from xblock.fragment import Fragment #DEPRECIATED
from web_fragments.fragment import Fragment

# import the hydrolearn custom text xblock
from hl_text import hl_text_XBlock


class HL_LearningActivity_XBlock(StudioContainerXBlockMixin, XBlock):

    # modify path to the custom starter template for empty xblocks
    #empty_template = 'templates/initial_learning_activity_template.html'

    display_name = String(
        display_name="Learning Activity",
        help="This name appears in the horizontal navigation at the top of the page",
        scope=Scope.settings,
        default="Learning Activity"
    )

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

        return fragment


    def author_edit_view(self, context):
        """
        Child blocks can override this to control the view shown to authors in Studio when
        editing this block's children.
        """
        fragment = Fragment()
        self.render_children(context, fragment, can_reorder=True, can_add=True)
        return fragment


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
