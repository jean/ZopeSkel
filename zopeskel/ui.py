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

def list_sorted_templates(filter_group=False):
    """
    Returns list of categories and templates.

    If "filter_group" is True, then this explictly filters to
    things provided by the ZopeSkel package--thereby hiding any
    templates the user may have on their system that sit on top
    of zopeskel's base classes. This is required in places where
    we want to generate canonical documents, and don't want to
    accidentally include things from the machine it's being run
    on.
    """
    
    cats = {}
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
        category = getattr(entry.load(), 'category', 'Uncategorized')
        cats.setdefault(category, []).append(entry)

    return cats
