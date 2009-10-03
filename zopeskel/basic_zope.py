import copy 
from zopeskel.basic_namespace import BasicNamespace
from zopeskel.base import get_var
from zopeskel.base import var, BooleanVar

VAR_ZOPE2 = BooleanVar(
        'zope2product',
        title='Zope2 Product?',
        description='Are you created a Zope2 product?',
        default=True,
        modes=(),
        help="""
Zope2 products will have a registration hook in their __init__.py,
used by the Zope2 machinery to handle any required processes during
server startup. Archetypes projects will require this, and all
projects for Zope2/Plone will benefit from it (even if not strictly
required, this allows the project to appear in places like the
Zope2 Control Panel list of products).

An appropriate time to choose False here would be if you are creating
a completely Zope3-only or non-Zope project.
"""
        )

class BasicZope(BasicNamespace):
    _template_dir = 'templates/basic_zope'
    summary = "A Zope project"
    help = """
This creates a Zope project without any specific Plone features.

This template expects a name in the form 'mycompany.myproject'
(1 dot, a 'basic namespace'); you cannot have a flat package name (no
dots, 'myproduct') or a nested namespace (2 dots, 
'collective.company.product')
"""
    required_templates = ['basic_namespace']
    use_cheetah = True

    vars = copy.deepcopy(BasicNamespace.vars)
    get_var(vars, 'namespace_package').default = 'myzopelib'
    get_var(vars, 'package').default = 'example'
    vars.insert(4, VAR_ZOPE2)


