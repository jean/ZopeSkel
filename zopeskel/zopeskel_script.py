import sys
import pkg_resources
from paste.script.command import get_commands

from zopeskel.ui import list_sorted_templates

USAGE = """
Usage:

    zopeskel <template> <output-name> [var1=value] ... [varN=value]

Common templates:

%s
Less common templates:

%s
For further help information, please invoke this script with the
option "--help".
"""

DESCRIPTION = """
This script allows you to create basic skeletons for plone and zope
products and buildouts based on best-practice templates.

It is a wrapper around PasteScript ("paster"), providing an easier
syntax for invoking and better help.


INVOKING THIS SCRIPT:

Basic usage:

    bin/zopeskel <template>

For example:

    bin/zopeskel archetypes

To create an Archetypes-based product for Plone. This will prompt you
for the name of your product, and for other information about it.

If you to specify your output name (resulting product, egg, or buildout,
depending on the template being used), you can also do so:

    zopeskel <template> <output-name>

For example:

    zopeskel archetypes Products.Example

In addition, you can pass variables to this that would be requested
by that template, and these will then be used. This is an advanced
feature mostly useful for scripted use of this:

    zopeskel archetypes Products.Example author_email=joel@joelburton.com

(You can specify as many of these as you want, in name=value pairs.
To get the list of variables that a template expects, you can ask for
this with "paster create -t <template-name> --list-variables").


ANSWERING QUESTIONS:

While being prompted on each question, you can enter with a single
question mark to receive interactive help for that question.


PROVIDING DEFAULTS:

It is also possible to set up default values to be used for any template by
creating a file called '.zopeskel' in your home directory. This file
should be in INI format.

For example, our $HOME/.zopeskel could contain:

    [DEFAULT]
    author_email = joel@joelburton.com
    license_name = GPL
    master_keywords = my common keywords here

    [plone3_theme]
    empty_styles = False
    license_name = BSD
    keywords = %(master_keywords)s additional keywords

Notes:

1) "empty_styles" applies only to themes; we can make this setting
   in the template-specific section of this file. This setting will
   not be used for other templates.

2) For a common setting, like our email address, we can set this in
   a section called DEFAULT; settings made in this section are used
   for all templates.

3) We can make a setting in DEFAULT and then override it for a
   particular template. In this example, we generally prefer the GPL,
   but issue our themes under the BSD license.

4) You can refer to variables from the same section or from the
   DEFAULT section using Python string formatting. In this example,
   we have a common set of keywords set in DEFAULT and extend it
   for the theming template by referring to the master list.


QUESTIONS

If you have further questions about the usage of bin/zopeskel, please feel
free to post your questions to the zopeskel mailing list or jump onto the
plone IRC channel (#plone) at irc.freenode.net.


To see the templates supported, run this script without any options.
"""

DOT_HELP = {
  0: """
This template expects a project name with no dots in it (a simple
Python package name, like 'foo').
""",
  1: """
This template expects a project name with 1 dot in it (a 'basic
namespace', like 'foo.bar').
""",
  2: """
This template expects a project name with 2 dots in it (a 'nested
namespace', like 'foo.bar.baz').
"""
}

def checkdots(template, name):
    """Check if project name appears legal, given template requirements.

    Templates can provide number of namespaces they expect (provided
    in 'ndots' attributes for number-of-dots in name). This checks that
    provided project name is has correct number of namespaces and that
    each part is a legal Python identifier.
    """

    ndots = getattr(template, 'ndots', None)
    if ndots is None: return   # No validation possible

    cdots = name.count(".")
    if ndots != cdots:
        raise ValueError(
            "Project name expected %i dots, supplied '%s' has %i dots" % (
                ndots, name, cdots))
    for part in name.split("."):
        # Check if Python identifier, http://code.activestate.com/recipes/413487/
        try:
            class test(object): __slots__ = [part]
        except TypeError:
            raise ValueError(
                "Not a valid Python dotted name: %s ('%s' is not an identifier)" % (name, part))


    
def usage():
    common, uncommon = list_printable_templates()
    print USAGE % (common, uncommon)

def show_help():
    print DESCRIPTION

def list_printable_templates():
    """
    Output a printable list of all templates, sorted into two parts.

    Templates will be sorted into 'common' and 'advanced' groups
    and listed separately.
    """
    common, advanced = list_sorted_templates()
    everyone = common + advanced
    max_name = max([len(e.name) for e in everyone])

    def display(entry):
        template = entry.load()
        return "|  %s:%s %s\n" % (
                entry.name,
                ' '*(max_name-len(entry.name)),
                template.summary)

    common = ''.join(map(display, common))
    advanced = ''.join(map(display, advanced))

    return common, advanced

def process_args():
    """ return a tuple of template_name, output_name and everything else
    
        everything else will be returned as a dictionary of key/value pairs
    """
    args = sys.argv[1:]
    try:
        template_name = args.pop(0)
    except IndexError:
        raise SyntaxError('No template name provided')
    output_name = None
    others = {}
    for arg in args:
        eq_index = arg.find('=')
        if eq_index == -1 and not output_name:
            output_name = arg
        elif eq_index > 0:
            key, val = arg.split('=')
            others[key] = val
        else:
            raise SyntaxError(arg)

    return template_name, output_name, others

def run():
    """ """

    if "--help" in sys.argv:
        show_help()
        return

    if len(sys.argv) == 1:
        usage()
        return
    
    try:
        template_name, output_name, opts = process_args()
    except SyntaxError, e:
        print "Error: There was a problem with your arguments: %s\n" % e
    
    rez = pkg_resources.iter_entry_points(
            'paste.paster_create_template',
            template_name)
    rez = list(rez)
    if not rez:
        usage()
        print "ERROR: No such template: %s\n" % template_name
        return

    template = rez[0].load()

    print "\n%s: %s" % (template_name, template.summary)
    help = getattr(template, 'help', None)
    if help:
        print template.help

    create = get_commands()['create'].load()
    
    command = create('create')

    if output_name:
        try:
            checkdots(template, output_name)
        except ValueError, e:
            print "ERROR: %s\n" % e
            return

    else:
        ndots = getattr(template, 'ndots', None)
        help = DOT_HELP.get(ndots)

        while True:
            if help: print help
            try:
                output_name = command.challenge("Enter project name")
                checkdots(template, output_name)
            except ValueError, e:
                print "\nERROR: %s" % e
            else:
                break
            

    print """
If at any point, you need additional help for a question, you can enter 
'?' and press RETURN.
"""

    optslist = [ '%s=%s' % (k,v) for k, v in opts.items() ]
    if output_name is not None:
        optslist.insert(0, output_name)
    command.run( [ '-q', '-t', template_name ] + optslist )


