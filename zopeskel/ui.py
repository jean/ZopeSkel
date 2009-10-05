"""
Module containing some common UI components that are useful for all user
interfaces, ie the console and the web interfaces.
"""
import pkg_resources

from zopeskel.base import BaseTemplate

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

def list_sorted_templates(filter_group=False):
    """
    Returns two part list of template entry points.

    Templates will be sorted into 'common' and 'advanced' groups
    and listed separately.
    """
    common_list = []
    advanced_list = []
    # grab a list of all paster create template entry points
    if filter_group:
        t_e_ps = pkg_resources.get_entry_map(
            'zopeskel')['paste.paster_create_template'].values()
    else:
        t_e_ps = pkg_resources.iter_entry_points('paste.paster_create_template')
    templates = []
    for entry in t_e_ps:
        try:
            # We only want our templates in this list
            template = entry.load()
            if issubclass(template, BaseTemplate):
                templates.append(entry)
        except Exception, e:
            # We will not be stopped!
            print 'Warning: could not load entry point %s (%s: %s)' % (
                entry.name, e.__class__.__name__, e)
    templates.sort(key=lambda x: x.name)

    for entry in templates:
        if entry.name in COMMON:
            common_list.append(entry)
        else:
            advanced_list.append(entry)

    return common_list, advanced_list
