import sys

# These are the "common" templates; they will be listed in a separate
# list for new users. Please be conservative about adding new
# templates to this list--we don't want it to be overwhelming.
# Users also see the "non-common" templates, just in a different
# listing; this is where things like PAS plugins, special hosting,
# Silva, etc., should remain.

COMMON = [
  'archetype',
  'plone',
  'plone2.5_buildout',
  'plone2.5_theme',
  'plone2_theme',
  'plone3_buildout',
  'plone3_portlet',
  'plone3_theme',
  'plone_app',
]

USAGE = "bin/zopeskel <template> <output-name> [var1=value] ... [varN=value]"

DESCRIPTION = """
bin/zopeskel allows the user to create basic skeletons for plone and zope
products and buildouts based on best-practice templates. 

To create a new skeleton, simply type bin/zopeskel followed by the name of
a template and the name you would like to give your new product or buildout.
Additionally, you may pre-answer any of the questions that zopeskel will ask
for a given template by providing 'name=value' pairs on the command line
after the name of your new product/buildout.  
"""
