from zopeskel.base import BaseTemplate
from zopeskel.base import var, EASY, EXPERT
from zopeskel.vars import StringVar
from zopeskel.plone3_buildout import (
    VAR_Z2_INSTALL, VAR_ZOPE_USER, VAR_ZOPE_PASSWD, VAR_HTTP, 
    VAR_DEBUG_MODE, VAR_VERBOSE_SEC )


class Zope2Buildout(BaseTemplate):
    _template_dir = 'templates/zope2_buildout'
    summary = "A buildout for a blank (non-Silva, non-Plone) Zope 2 instance"
    help = """
This template creates a buildout that does not contain Plone or Silva
information. It is intended for people using Zope 2 directly. If you
would like to use Plone or Silva, you should use the appropriate buildouts.
"""
    required_templates = []
    use_cheetah = True

    vars = [
        VAR_Z2_INSTALL,
        StringVar(
            'zope2_version',
            title='Zope 2 Version',
            description='Version of Zope 2 to fetch, if needed',
            modes=(EASY, EXPERT),
            page='Main',
            default='2.11.1',
            help="""
If a version of Zope needs to be pulled down, this option lets you
specify the version.
"""
            ),
        VAR_ZOPE_USER,
        VAR_ZOPE_PASSWD,
        VAR_HTTP,
        VAR_DEBUG_MODE,
        VAR_VERBOSE_SEC,
        ]

    def post(self, command, output_dir, vars):
        print "-----------------------------------------------------------"
        print "Generation finished"
        print "You probably want to run python bootstrap.py and then edit"
        print "buildout.cfg before running bin/buildout -v"
        print
        print "See README.txt for details"
        print "-----------------------------------------------------------"
        super(Zope2Buildout, self).post(command, output_dir, vars)



