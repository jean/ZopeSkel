import copy

from zopeskel.nested_namespace import NestedNamespace
from zopeskel.base import get_var

class PlonePas(NestedNamespace):
    _template_dir = 'templates/plone_pas'
    summary = "A project for a Plone PAS plugin"
    help = """
This create a project for developing a PAS ('pluggable authentication
system') plugin.

This template expects a name in the form 'plone.app.myproject' (2 dots, a 
'nested namespace'). You cannot have a flat package name (no dots, 
'myproduct') or a basic namespace (1 dot, 'plone.myproject').
"""
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

