import copy

from zopeskel.base import get_var
from zopeskel.base import var, EXPERT, EASY
from zopeskel.basic_namespace import BasicNamespace
from zopeskel.vars import DottedVar

VAR_NS2 = DottedVar(
            'namespace_package2', 
            title='Namespace 2 Package Name',
            description='Name of second outer namespace package',
            default='plone', 
            modes=(EXPERT,), 
            page='Namespaces',
            help="""
This is the name of the second outer package (Python folder) for this
project. For example, in 'plone.app.example', this would be
'plone' ('app' will be the first namespace, and 'example' would be
the package name). 

This will often be the name of your company/project, or a common-style 
name like (for Plone products) 'collective'.
"""
)

class NestedNamespace(BasicNamespace):
    _template_dir = 'templates/nested_namespace'
    summary = "A basic Python project with two nested namespaces"
    help = """
This creates a Python project without any Zope or Plone features.

This template expects a name in the form 'mycompany.myapp.myproject'
(2 dots). To have a flat package name (no dots, 'myproject'), use the 
'basic_package' template. To use a a single namespace (1 dot, 
'mycompany.project'), use the 'basic_namespace' template.
"""
    required_templates = []
    use_cheetah = True

    vars = copy.deepcopy(BasicNamespace.vars)
    get_var(vars, 'namespace_package').default = 'plone'
    vars.insert(2, VAR_NS2)
    get_var(vars, 'package').default = 'example'


