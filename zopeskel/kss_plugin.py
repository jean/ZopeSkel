# -*- coding: utf-8 -*-
import copy

from zopeskel.base import get_var
from zopeskel.base import var
from zopeskel.basic_namespace import BasicNamespace
from zopeskel.nested_namespace import VAR_NS2


class KssPlugin(BasicNamespace):
    _template_dir = 'templates/kss_plugin'
    summary = "A project for a KSS plugin"
    help = """
This creates a project for a KSS plugins ('Kinetic Style Sheets', a 
Plone 3 framwork for JavaScript/AJAX).

This template expects a name in the form 'mycompany.kss.example'
(2 dot, a 'nested namespace'); you cannot have a flat package name 
(no dots, 'myproduct') or a single namespace (1 dot, 'mycompany.product').
"""

    required_templates = []
    use_cheetah = True

    vars = copy.deepcopy(BasicNamespace.vars)
    get_var(vars, 'namespace_package').default = 'kss'
    vars.insert(2, VAR_NS2)
    get_var(vars, 'keywords').default = 'kss plugin'
