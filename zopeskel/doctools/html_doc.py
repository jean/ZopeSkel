#!/usr/bin/python

from zopeskel.ui import list_sorted_templates

def make_html():

    common, advanced = list_sorted_templates()
    for title, list_ in (
            ('Common Recipes', common), 
            ('Advanced Recipes', advanced)):
        print "<h2>%s</h2>" % title
        for temp in list_:
            print "<h3>%s</h3>" % temp.name
            tempc = temp.load()
            print '<p class="summary">%s</p>' % tempc.summary
            help = getattr(tempc, 'help', '')
            for para in help.split("\n\n"):
                print '<p>%s</p>' % para
            print "<ul>"
            for var in tempc.vars:
                if hasattr(var, 'pretty_description'):
                    print "<li>%s</li>" % var.pretty_description()
                else:
                    print "<li>%s</li>" % var.name
            print "</ul>"
            
if __name__=="__main__":
    make_html()
