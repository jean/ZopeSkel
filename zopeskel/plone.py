import copy

from zopeskel.basic_zope import BasicZope
from zopeskel.base import get_var
from zopeskel.base import var

class Plone(BasicZope):
    _template_dir = 'templates/plone'
    summary = "A Plone project"
    required_templates = ['basic_namespace']
    use_local_commands = True
    use_cheetah = True
    vars = copy.deepcopy(BasicNamespace.vars)
    get_var(vars, 'namespace_package').default = 'plone'
    get_var(vars, 'package').default = 'example'
    get_var(vars, 'author').default = ''
    get_var(vars, 'author_email').default = ''
    get_var(vars, 'url').default = 'http://svn.plone.org/svn/plone/plone.example'


