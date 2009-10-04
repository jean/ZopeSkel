import copy

from zopeskel.nested_namespace import NestedNamespace
from zopeskel.base import get_var
from zopeskel.base import var
from zopeskel.basic_zope import VAR_ZOPE2

class PloneApp(NestedNamespace):
    _template_dir = 'templates/plone_app'
    summary = "A project for Plone products with a nested namespace (2 dots in name)"
    help = """
This creates a Plone project (to create a Plone *site*, you probably
want to use the one of the templates for a buildout).

To create a Plone project with a name like 'mycompany.myproject' (1 dot,
a 'basic namespace'), use the 'plone' template instead.
"""
    required_templates = ['nested_namespace']
    use_cheetah = True

    vars = copy.deepcopy(NestedNamespace.vars)
    vars.insert(4, VAR_ZOPE2) 
    get_var(vars, 'author').default = ''
    get_var(vars, 'author_email').default = ''
    get_var(vars, 'url').default = 'http://svn.plone.org/svn/plone/plone.app.example'

