#!/usr/bin/python

"""HTML documentation generator.

A quick-n-dirty generator of HTML docs on templates, including their
fields and subtemplates.
"""

# This should be changed into generating data structures, and having
# Cheetah templates to render them

from zopeskel.ui import list_sorted_templates
import pkg_resources

def _get_local_commands():
    """Return dict of main_template -> [ local template1, ... localN ]"""

    out = {}
    for entry in pkg_resources.iter_entry_points('zopeskel.zopeskel_sub_template'):
        localc = entry.load()
        for parent in localc.parent_templates:
            out.setdefault(parent, []).append((entry.name, localc.summary))
    return out

def make_html():

    common, advanced = list_sorted_templates(filter_group=True)
    subtemplates = _get_local_commands()

    for title, list_ in (
            ('Common Templates', common),
            ('Advanced Templates', advanced)):
        print "<h2>%s</h2>" % title
        for temp in list_:
            print "<h3>%s</h3>" % temp.name
            tempc = temp.load()
            print '<p class="summary">%s</p>' % tempc.summary
            help = getattr(tempc, 'help', '')
            for para in help.split("\n\n"):
                print '<p>%s</p>' % para
            print "<h4>Fields:</h4>"
            print "<ul>"
            for var in tempc.vars:
                if hasattr(var, 'pretty_description'):
                    print "<li>%s</li>" % var.pretty_description()
                else:
                    print "<li>%s</li>" % var.name
            print "</ul>"
            subs = subtemplates.get(temp.name)
            if subs:
                print "<h4>Sub Templates:</h4>"
                print "<ul>"
                for sub in subs:
                    print "<li>%s (%s)</li>" % (sub[0], sub[1])
                print "</ul>"

if __name__=="__main__":
    make_html()
