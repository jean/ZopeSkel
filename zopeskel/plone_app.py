import copy

from zopeskel.nested_namespace import NestedNamespace
from zopeskel.base import get_var
from zopeskel.base import var
from zopeskel.basic_zope import VAR_ZOPE2

class PloneApp(NestedNamespace):
    _template_dir = 'templates/plone_app'
    summary = "A Plone App project"
    required_templates = ['nested_namespace']
    use_cheetah = True

    vars = copy.deepcopy(NestedNamespace.vars)
    vars.insert(4, VAR_ZOPE2) 
    get_var(vars, 'author').default = ''
    get_var(vars, 'author_email').default = ''
    get_var(vars, 'url').default = 'http://svn.plone.org/svn/plone/plone.app.example'

