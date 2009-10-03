from zopeskel.base import BaseTemplate
from zopeskel.base import var, EASY, EXPERT
from zopeskel.vars import StringVar, BooleanVar, IntVar, OnOffVar

VAR_PLONEVER = StringVar(
    'plone_version',
    title='Plone Version',
    description='Plone version # to install',
    default='3.3.1',
    modes=(EASY,EXPERT),
    page='Main',
    help="""
This is the version of Plone that will be used for this buildout.
You should enter the version number you wish to use.
"""
    )

VAR_Z2_INSTALL = StringVar(
    'zope2_install',
    title='Zope2 Install Path',
    description='Path to Zope2 installation; leave blank to fetch one!',
    default='',
    modes=(EASY,EXPERT),
    page='Main',
    help="""
This is the file path to the Zope 2 installation. You can enter this
path to use a pre-existing installation, or you can leave it blank, and
the current Zope 2 will be downloaded and installed in your new
buildout.
"""
    )

VAR_PLONE_PRODUCTS = StringVar(
    'plone_products_install',
    title='Plone Products Directory',
    description='Path to directory containing Plone products; leave blank to fetch one',
    modes=(EASY, EXPERT),
    page='Main',
    default='',
    help="""
TODO
"""
    )

VAR_ZOPE_USER = StringVar(
    'zope_user',
    title='Initial Zope Username',
    description='Username for Zope root admin user',
    modes=(EASY, EXPERT),
    page='Main',
    default='admin',
    help="""
Your buildout will have a single user, with manager privileges, defined
at the root. This option lets you select the name for this user.
"""
    )

VAR_ZOPE_PASSWD = StringVar(
    'zope_password',
    title='Initial User Password',
    description='Password for Zope root admin user',
    modes=(EASY, EXPERT),
    page='Main',
    default='',
    help="""
Your buildout will have a single user, "%(zope_user)s", with manager 
privileges, defined at the root. This option lets you select the initial
password for this user. If left blank, the password will be randomly
generated.
"""
    )

VAR_HTTP = IntVar(
    'http_port',
    title='HTTP Port',
    description='Port that Zope will use for serving HTTP',
    default='8080',
    modes=(EXPERT,EASY),
    page='Main',
    help="""
This options lets you select the port # that Zope will use for serving
HTTP.
"""
    )

VAR_DEBUG_MODE = OnOffVar(
    'debug_mode',
    title='Debug Mode',
    description='Should debug mode be "on" or "off"?',
    default='off',
    modes=(EXPERT,EASY),
    page='Main',
    help="""
Debug mode (sometimes called "Debug/Development Mode") is the correct
setting for running a site under development--it ensures that on-disk
changes to templates and skin scripts are immediately visible, and
allows use of certain add-on debugging/profiling products. Running your
Zope in the foreground (with "bin/plonectl fg" or similar commands)
always puts you in debug mode; this setting controls whether you are
in debug mode even when running in the background.

You should set this to "on" during development; once you are ready to
deploy your site, you change this to "off" in your buildout.cfg.
"""
    )

VAR_VERBOSE_SEC = OnOffVar(
        'verbose_security',
        title='Verbose Security?',
        description='Should verbose security be "on" or "off"?',
        default='off',
        modes=(EASY, EXPERT),
        page='Main',
        help="""
Security error messages (such as "Unauthorized" errors) in Plone are
intentionally vague--the system doesn't want to reveal too much about
the security configuration in error messages, given that those error
messages may be inappropriately printed out/shared/email and intercepted
by others.

"Verbose security" is a buildout setting that enables significantly more
helpful, detailed unauthorized error messages.

There may be a small security risk in leaving this enabled on a site in
deployment; if you turn it on, you should consider turning it off.
"""
        )



class Plone3Buildout(BaseTemplate):
    _template_dir = 'templates/plone3_buildout'
    summary = "A buildout for Plone 3 installation"
    required_templates = []
    use_cheetah = True

    vars = [ VAR_PLONEVER,
             VAR_Z2_INSTALL,
             VAR_PLONE_PRODUCTS,
             VAR_ZOPE_USER,
             VAR_ZOPE_PASSWD,
             VAR_HTTP,
             VAR_DEBUG_MODE,
             VAR_VERBOSE_SEC,
        ]

    def pre(self, command, output_dir, vars):
        vars['oldplone'] = vars['plone_version'].startswith("3.0") or \
                            vars['plone_version'].startswith("3.1")
        vars['veryoldplone'] = vars['plone_version'].startswith("2.")
        if vars['veryoldplone']:
            vars['zope2_version'] = "2.9.10"
        vars['newplone'] = not vars['veryoldplone'] and not vars['oldplone']
        super(Plone3Buildout, self).pre(command, output_dir, vars)
    
    def post(self, command, output_dir, vars):
        print "-----------------------------------------------------------"
        print "Generation finished"
        print "You probably want to run python bootstrap.py and then edit"
        print "buildout.cfg before running bin/buildout -v"
        print
        print "See README.txt for details"
        print "-----------------------------------------------------------"



