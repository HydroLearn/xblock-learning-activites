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

# from xblock.fragment import Fragment #DEPRECIATED
from web_fragments.fragment import Fragment

# import the hydrolearn custom text xblock
from hl_text import HLCustomTextXBlock


class HL_LearningActivity_XBlock(HLCustomTextXBlock):

    # modify path to the custom starter template for empty xblocks
    #empty_template = 'templates/initial_learning_activity_template.html'

    display_name = String(
        display_name="Learning Activity",
        help="This name appears in the horizontal navigation at the top of the page",
        scope=Scope.settings,
        default="Learning Activity"
    )

    # def get_empty_template_name(self):
    #     return 'templates/initial_learning_activity_template.html'
    def get_empty_template(self, context={}):
        return render_template('templates/initial_learning_activity_template.html', context)
