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

USAGE = "bin/zopeskel <template> <output-name> [var1=value] ... [varN=value]"

DESCRIPTION = """
bin/zopeskel allows the user to create basic skeletons for plone and zope
products and buildouts based on best-practice templates. 

To create a new skeleton, simply type bin/zopeskel followed by the name of
a template and the name you would like to give your new product or buildout.
Additionally, you may pre-answer any of the questions that zopeskel will ask
for a given template by providing 'name=value' pairs on the command line
after the name of your new product/buildout.  You probably don't want to do
this until you are more familiar with the specific questions in a given
template.

It is also possible to set up default values to be used for any template by
creating a file called '.zopeskel' in your home directory.  This file must be
in INI format.  For example:

<place sample here>


If you have further questions about the usage of bin/zopeskel, please feel
free to post your questions to the zopeskel mailing list or jump onto the 
plone IRC channel (#plone) at irc.freenode.net.
"""

def list_sorted_templates():
    """ output a printable list of all templates, sorted into two parts
        
        templates will be sorted into 'common' and 'advanced' groups
        and listed separately.
    """
    common_list = ""
    advanced_list = ""
    # grab a list of all paster create template entry points
    t_e_ps = pkg_resources.iter_entry_points('paster.paster_create_template')
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
