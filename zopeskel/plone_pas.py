import copy

from zopeskel.nested_namespace import NestedNamespace
from zopeskel.base import get_var

class PlonePas(NestedNamespace):
    _template_dir = 'templates/plone_pas'
    summary = "A Plone PAS project"
    required_templates = ['nested_namespace']
    use_cheetah = True
    use_local_commands = True

    vars = copy.deepcopy(NestedNamespace.vars)
    get_var(vars, 'namespace_package2').default = 'pas'
    get_var(vars, 'author').default = ''
    get_var(vars, 'author_email').default = ''
    get_var(vars, 'url').default = 'http://svn.plone.org/svn/plone/pas.plugin.example'

    def pre(self, command, output_dir, vars):
      vars['multiplugin_name'] = vars['package'].title()

