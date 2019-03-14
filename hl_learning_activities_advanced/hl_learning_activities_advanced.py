"""
    Advanced Learning activities xblock

    xblock for generating learning activities as a parent container
    containing a collection of child blocks representing instructional
    steps for completing the activity

"""

import urllib, datetime, json, urllib2, logging

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



class HL_LearningActivity_advanced_XBlock(
    XBlock,
    StudioEditableXBlockMixin,
    StudioContainerWithNestedXBlocksMixin,
    XBlockWithPreviewMixin,
):


    ############################################
    # Activity properties
    ############################################

    CATEGORY = "hl_learning_activity_advanced"
    STUDIO_LABEL = "Activity"

    # modify path to the custom starter template for empty xblocks
    # empty_template = 'templates/initial_learning_activity_template.html'
    has_children = True

    # CHILD_PREVIEW_TEMPLATE = "templates/default_preview_view.html"

    display_name = String(
        display_name="Display Name",
        help="This name appears in the horizontal navigation at the top of the page",
        scope=Scope.settings,
        default="Learning Activity (Advanced)"
    )

    editable_fields = ['display_name']



    def get_empty_template(self, context={}):

        return loader.render_django_template('templates/initial_learning_activity_template.html', context)


    def studio_view(self, context):

        fragment = super(HL_LearningActivity_advanced_XBlock, self).studio_view(context)

        fragment.add_content(loader.render_django_template('templates/hl_learning_activity-cms.html', context))

        fragment.add_css(loader.load_unicode('static/css/hl_learning_activity-cms.css'))
        fragment.add_javascript(loader.load_unicode('static/js/hl_learning_activity-cms.js'))
        fragment.initialize_js('Learning_Activity_Studio')

        return fragment

    def student_view(self, context):

        # import for type checking children
        from .child_blocks import la_step
        from .child_blocks import la_intro

        fragment = Fragment()


        child_content = u""
        instructions = u""

        ## TODO: make this better

        #  old add_frag_resources   =  add_fragment_resources
        #  old add_frags_resources   =  add_resources


        # gather the instructions
        for child_id in self.children:
            child = self.runtime.get_block(child_id)

            if child is None:
                child_content += u"<p>[{}]</p>".format(self._(u"Error: Unable to load child component."))

            if isinstance(child, la_step):
                child_fragment = child.render('student_view', context)
                fragment.add_fragment_resources(child_fragment)
                child_content += child_fragment.content




        # fragment.add_content(loader.render_django_template('templates/html/mentoring.html', {
        #     'self': self,
        #     'child_content': child_content,
        #     'instructions': instructions,
        # }, i18n_service=self.i18n_service))

        context['child_content'] = child_content

        fragment.add_content(loader.render_django_template('templates/hl_learning_activity-lms.html', context))

        fragment.add_css(loader.load_unicode('static/css/hl_learning_activity-lms.css'))
        fragment.add_javascript(loader.load_unicode('static/js/hl_learning_activity-lms.js'))
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


    ############################################
    # StudioContainerWithNestedXBlocksMixin overrides
    ############################################
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
                label=_(u"Introduction"),
                # boilerplate='studio_default',
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
                label=_(u"Activity Step"),
                # boilerplate='studio_default',
            ))
        except ImportError:
            # LOG.warning('Failed to Load HL Text block.')
            log.warning("Failed to import 'Step' activity component.")
            pass



        try:

            additional_blocks.append(NestedXBlockSpec(
                hl_text_XBlock,
                single_instance=False,
                disabled=False,
                label=_(u"Text"),
                # boilerplate='hl-text-boiler',
            ))
        except ImportError:
            # LOG.warning('Failed to Load HL Text block.')
            log.warning("Failed to import 'Introduction' activity component.")
            pass


        return additional_blocks


    # def author_edit_view(self, context):
    #     """
    #     Child blocks can override this to control the view shown to authors in Studio when
    #     editing this block's children.
    #     """
    #     fragment = Fragment()
    #     self.render_children(context, fragment, can_reorder=True, can_add=True)
    #     return fragment
    #

    def author_preview_view(self, context):
        """
        Child blocks can override this to add a custom preview shown to authors in Studio when
        not editing this block's children.
        """
        return self.student_view(context)

    # def preview_view(self, context):
    #     """
    #         Preview view - used by StudioContainerWithNestedXBlocksMixin to render nested xblocks in preview context.
    #         Default implementation uses author_view if available, otherwise falls back to student_view
    #         Child classes can override this method to control their presentation in preview context
    #     """
    #     return self.student_view(context)


