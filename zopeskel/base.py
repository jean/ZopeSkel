import os
import ConfigParser
from paste.script import pluginlib
from paste.script import templates
from paste.script.templates import var as base_var
from paste.script.command import BadCommand
from paste.script.templates import BasicPackage

LICENSE_CATEGORIES = {
    'DFSG' : 'License :: DFSG approved',
    'EFS' : 'License :: Eiffel Forum License (EFL)',
    'NPL' : 'License :: Netscape Public License (NPL)',
    'ASL' : 'License :: OSI Approved :: Apache Software License',
    'BSD' : 'License :: OSI Approved :: BSD License',
    'FDL' : 'License :: OSI Approved :: GNU Free Documentation License (FDL)',
    'GPL' : 'License :: OSI Approved :: GNU General Public License (GPL)',
    'LGPL' : 'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
    'MIT' : 'License :: OSI Approved :: MIT License',
    'MPL' : 'License :: OSI Approved :: Mozilla Public License 1.0 (MPL)',
    'MPL11' : 'License :: OSI Approved :: Mozilla Public License 1.1 (MPL 1.1)',
    'QPL' : 'License :: OSI Approved :: Qt Public License (QPL)',
    'ZPL' : 'License :: OSI Approved :: Zope Public License',
    }

def get_var(vars, name):
    for var in vars:
        if var.name == name:
            return var
    else:
        raise ValueError("No such var: %r" % name)


def update_setup_cfg(path, section, option, value):
    
    parser = ConfigParser.ConfigParser()
    if os.path.exists(path):
        parser.read(path)

    if not parser.has_section(section):
        parser.add_section(section)

    parser.set(section, option, value)
    parser.write(open(path, 'w'))


class BaseTemplate(templates.Template):
    """Base template for all ZopeSkel templates"""

    #a zopeskel template has to set this to True if it wants to use 
    #localcommand
    use_local_commands = False

    #this is just to be able to add ZopeSkel to the list of paster_plugins if
    #the use_local_commands is set to true and to write a zopeskel section in 
    #setup.cfg file containing the name of the parent template. 
    #it will be used by addcontent command to list the apropriate subtemplates 
    #for the generated project. the post method is not a candidate because 
    #many templates override it
    def run(self, command, output_dir, vars):
        
        if self.use_local_commands and 'ZopeSkel' not in self.egg_plugins:
            self.egg_plugins.append('ZopeSkel')

        templates.Template.run(self, command, output_dir, vars)

        setup_cfg = os.path.join(output_dir, 'setup.cfg')
        if self.use_local_commands:
            update_setup_cfg(setup_cfg, 'zopeskel', 'template', self.name)

    def print_subtemplate_notice(self, output_dir=None):
            """Print a notice about local commands begin availabe (if this is
            indeed the case).
    
            Unfortunately for us, at this stage in the process, the
            egg_info directory has not yet been created (and won't be
            within the scope of this template running [see
            paste.script.create_distro.py]), so we're cannot show which
            subtemplates are available.
            """
            plugins = pluginlib.resolve_plugins(['ZopeSkel'])
            commands = pluginlib.load_commands_from_plugins(plugins)
            if not commands:
                return
            commands = commands.items()
            commands.sort()
            longest = max([len(n) for n, c in commands])
            print_commands = []
            for name, command in commands:
                name = name + ' ' * (longest - len(name))
                print_commands.append('  %s  %s' % (name,
                                                    command.load().summary))
            print_commands = '\n'.join(print_commands)
            print '-' * 78
            print """\
The project you just created has local commands. These can be used from within
the product.

usage: paster COMMAND

Commands:
%s

For more information: paster help COMMAND""" % print_commands
            print '-' * 78

    def post(self, *args, **kargs):
        if self.use_local_commands:
            self.print_subtemplate_notice()
        templates.Template.post(self, *args, **kargs)

    def check_vars(self, vars, cmd):
        # Copied and modified from PasteScript's check_vars--
        # the method there wasn't hookable for the things
        # we need -- question posing, validation, etc.
        # 
        # Admittedly, this could be merged into PasteScript,
        # but it was decided it was easier to limit scope of 
        # these changes to ZopeSkel, as other projects may
        # use PasteScript in very different ways.

        cmd._deleted_once = 1      # don't re-del package

        # now, mostly copied direct from paster
        expect_vars = self.read_vars(cmd)
        if not expect_vars:
            # Assume that variables aren't defined
            return vars
        converted_vars = {}
        unused_vars = vars.copy()
        errors = []

        # TODO: here is where we have to say some things won't be used

        #if var.name == 'button_easy' and converted_vars["button_easy"] == "True":
        #    unused_vars['author']=1
        #    unused_vars['author_email']=1
        #    unused_vars['long_description']=1
        #    unused_vars['url']=1
        #    unused_vars['version']=1
        #    unused_vars['keywords']=1
        #    unused_vars['license_name']=1

        for var in expect_vars:
            if var.name not in unused_vars:
                if cmd.interactive:
                    prompt = var.pretty_description()
                    response = cmd.challenge(prompt, var.default, var.should_echo)
                    converted_vars[var.name] = response
                elif var.default is command.NoDefault:
                    errors.append('Required variable missing: %s'
                                  % var.full_description())
                else:
                    converted_vars[var.name] = var.default
            else:
                converted_vars[var.name] = unused_vars.pop(var.name)


        if errors:
            raise command.BadCommand(
                'Errors in variables:\n%s' % '\n'.join(errors))
        converted_vars.update(unused_vars)
        vars.update(converted_vars)

        result = converted_vars

        package = vars["project"]
        result['namespace_package'], result['package'] = package.split(".")
        result['zip_safe']=False
        result['zope2product']=True

        if converted_vars['button_easy'] == "True":
            result['author']='Joel Burton'
            result['author_email']='joel@joelburton.com'
            result['long_description']=''
            result['url']=''
            result['version']='1.0'
            result['keywords']=''
            result['license_name']='GPL'

        return self._map_boolean(result)


##########################################################################
# Variable

class ValidationException(ValueError):
    """Invalid value provided for variable."""


class var(base_var):

    def __init__(self, name, description,
                 default='', should_echo=True,
                 title=None, help=None, widget=None, modes=('all',)):
        self.name = name
        self.description = description
        self.default = default
        self.should_echo = should_echo
        self.title = title
        self.help = help
        if not widget:
            self.widget = self._default_widget
        else:
            self.widget = widget
        self.modes = modes

    def pretty_description(self):
        title = getattr(self, 'title', self.name) or self.name

        if self.description:
            return '%s (%s)' % (title, self.description)
        else:
            return title

    def validate(self, value):
        raise NotImplementedError


class BooleanVar(var):
    _default_widget = 'boolean'

    def validate(self, value):
        #Get rid of bonus whitespace
        if isinstance(value, basestring):
            value = value.strip().lower()

        #Map special cases to correct values.
        if value in ['t', 'y', 'yes', 'true', 1]: 
            value = True
        elif value in ['f','n','no', 'false', 0]:
            value = False

        if type(value) != bool:
            raise ValidationException("Not a valid boolean value: %s" % value)

        return value


class StringVar(var):
    """Single string values."""

    _default_widget = 'string'

    def validate(self, value):
        if not isinstance(value, basestring):
            raise ValidationException("Not a string value: %s" % value)

        value = value.strip()

        return value


class TextVar(StringVar):
    """Multi-line values."""

    _default_widget = 'text'


class DottedVar(var):
    """Variable for 'dotted Python name', eg, 'foo.bar.baz'"""

    _default_widget = 'string'

    def validate(self, value):
        if not isinstance(value, basestring):
            raise ValidationException("Not a string value: %s" % value)
        value = value.strip()

        names = value.split(".")
        for name in names:
            # Check if Python identifier, http://code.activestate.com/recipes/413487/
            try:
                class test(object): __slots__ = [name]
            except TypeError:
                raise ValidationException("Not a valid Python dotted name: %s ('%s' is not an identifier)" % (value, name))

        return value
