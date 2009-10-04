# -*- coding: utf-8 -*-
import copy

from zopeskel.base import get_var
from zopeskel.base import var
from zopeskel.nested_namespace import NestedNamespace


class KssPlugin(NestedNamespace):
    _template_dir = 'templates/kss_plugin'
    summary = "A project for a KSS plugin"
    ndots = 2
    help = """
This creates a project for a KSS plugins ('Kinetic Style Sheets', a 
Plone 3 framwork for JavaScript/AJAX).
"""

    required_templates = []
    use_cheetah = True

    vars = copy.deepcopy(NestedNamespace.vars)
    get_var(vars, 'namespace_package').default = 'kss'
    get_var(vars, 'namespace_package2').default = 'plugin'
    get_var(vars, 'keywords').default = 'kss plugin'
