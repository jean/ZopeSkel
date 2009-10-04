from zopeskel.base import BaseTemplate
from zopeskel.base import BadCommand
from zopeskel.base import var, EASY, EXPERT
from zopeskel.base import templates
from zopeskel.vars import StringVar, StringChoiceVar
from zopeskel.plone3_buildout import (
    VAR_Z2_INSTALL, VAR_ZOPE_USER, VAR_ZOPE_PASSWD, VAR_HTTP, 
    VAR_DEBUG_MODE, VAR_VERBOSE_SEC )


class SilvaBuildout(BaseTemplate):
    _template_dir = 'templates/silva_buildout'
    summary = "A buildout for Silva projects"
    help = """
This template creates an installation of Silva 
(http://www.infrae.com/products/silva).
"""
    post_run_msg = """
Generation finished.

You probably want to run python bootstrap.py and then edit
buildout.cfg before running bin/buildout -v".

See README.txt for details.
"""
    required_templates = []
    use_cheetah = True

    vars = [
        VAR_Z2_INSTALL,
        StringChoiceVar(
            'silva_distribution',
            title='Silva Distribution',
            description='Version of Silva to install, "stable" or "development"',
            default="stable",
            modes=(EASY, EXPERT),
            page='Main',
            choices=('stable','development'),
            ),
        VAR_ZOPE_USER,
        VAR_ZOPE_PASSWD,
        VAR_HTTP,
        VAR_DEBUG_MODE,
        VAR_VERBOSE_SEC,
        ]
