
from hl_text import hl_text_XBlock

from xblockutils.resources import ResourceLoader
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

loader = ResourceLoader(__name__)

#############################################
# Child block types
#############################################

class la_intro(hl_text_XBlock):

    display_name = String(
            display_name="Introduction",
            help="This name appears in the horizontal navigation at the top of the page",
            scope=Scope.settings,
            default="Introduction"
        )

    def get_empty_template(self, context={}):
        return loader.render_template('templates/parts/intro_template.html', context)



class la_step(hl_text_XBlock):

    display_name = String(
            display_name="Activity Step",
            help="This name appears in the horizontal navigation at the top of the page",
            scope=Scope.settings,
            default="Activity Step"
        )

    def get_empty_template(self, context={}):
        return loader.render_template('templates/parts/step_template.html', context)


class la_checkin(XBlock):
    display_name = String(
            display_name="Activity Step",
            help="This name appears in the horizontal navigation at the top of the page",
            scope=Scope.settings,
            default="Activity Step"
        )

    question = String(
            display_name="Question",
            help="a question presented to the student",
            scope=Scope.content,
            default="Question..."
        )

    answer = String(
            display_name="Answer",
            help="The expected answer to the provided question",
            scope=Scope.content,
            default="Answer..."
        )

    hint = String(
            display_name="Hint",
            help="(OPTIONAL) a hint to help the user in forming an answer.",
            scope=Scope.content,
            default="question_text"
        )
