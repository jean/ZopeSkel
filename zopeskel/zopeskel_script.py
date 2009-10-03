import sys
import pkg_resources

# These are the "common" templates; they will be listed in a separate
# list for new users. Please be conservative about adding new
# templates to this list--we don't want it to be overwhelming.
# Users also see the "non-common" templates, just in a different
# listing; this is where things like PAS plugins, special hosting,
# Silva, etc., should remain.

COMMON = [
  'archetype',
  'plone',
  'plone2.5_buildout',
  'plone2.5_theme',
  'plone2_theme',
  'plone3_buildout',
  'plone3_portlet',
  'plone3_theme',
  'plone_app',
]

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

def list_sorted_templates():
    """Output a printable list of all templates, sorted into two parts.
        
    Templates will be sorted into 'common' and 'advanced' groups
    and listed separately.
    """
    common_list = ""
    advanced_list = ""
    # grab a list of all paster create template entry points
    t_e_ps = pkg_resources.iter_entry_points('paste.paster_create_template')
    templates = []
    for entry in t_e_ps:
        try:
            templates.append(entry.load()(entry.name))
        except Exception, e:
            # We will not be stopped!
            print 'Warning: could not load entry point %s (%s: %s)' % (
                entry.name, e.__class__.__name__, e)
    max_name = max([len(t.name) for t in templates])
    templates.sort(lambda a, b: cmp(a.name, b.name))
    
    for template in templates:
        name = template.name
        display = "|  %s:%s %s\n" % (
            name,
            ' '*(max_name-len(template.name)),
            template.summary)
        if name in COMMON:
            common_list += display
        else:
            advanced_list += display
    
    return common_list, advanced_list

def usage():
    common, uncommon = list_sorted_templates()
    print USAGE % (common, uncommon)

def help():
    print DESCRIPTION

def run():
    """ """
    # Do something cool
