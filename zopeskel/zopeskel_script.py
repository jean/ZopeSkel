import sys

USAGE = "bin/zopeskel <template> <package-name> [var1=value] . . . [varN=value]"

DESCRIPTION = """
bin/zopeskel allows the user to create basic skeletons for plone and zope
products and buildouts based on best-practice templates. 

To create a new skeleton, simply type bin/zopeskel followed by the name of
a template and the name you would like to give your new product or buildout.
Additionally, you may pre-answer any of the questions that zopeskel will ask
for a given template by providing 'name=value' pairs on the command line
after the name of your new product/buildout.  
"""