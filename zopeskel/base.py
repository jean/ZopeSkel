import os
import ConfigParser
from ConfigParser import SafeConfigParser
from paste.script import command
from paste.script import pluginlib
from paste.script import templates
from paste.script.templates import var as base_var
from paste.script.command import BadCommand
from paste.script.templates import BasicPackage
from zopeskel.vars import var, BooleanVar
from zopeskel.vars import EASY, EXPERT


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

def get_zopeskel_prefs():
    # http://snipplr.com/view/7354/get-home-directory-path--in-python-win-lin-other/
    try:
        from win32com.shell import shellcon, shell
        homedir = shell.SHGetFolderPath(0, shellcon.CSIDL_APPDATA, 0, 0)
    except ImportError: # quick semi-nasty fallback for non-windows/win32com case
        homedir = os.path.expanduser("~")

    # Get defaults from .zopeskel
    config = SafeConfigParser()
    config.read('%s/.zopeskel' % homedir)
    return config

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

    vars = [
        BooleanVar(
            'expert_mode',
            title='Expert Mode?',
            description='Would you like to run zopeskel in expert mode?',
            page='Main',
            default='False',
            help="""
In Expert Mode, you will be asked to answer a larger
number of questions during this setup process.  Most
users should not run in expert mode.
"""),
    ]

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
            paste.script.create_distro.py]), so we cannot show which
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

    def _filter_for_modes(self, expert_mode, expected_vars):
        """ given the boolean 'expert_mode' and a list of expected vars,
            return a dict of vars to be hidden from view
        """
        hidden = {}
        for var in expected_vars:
            # if in expert mode, hide vars not for expert mode
            if expert_mode and EXPERT not in var.modes:
                hidden[var.name] = 1

            if not expert_mode and EASY not in var.modes:
                hidden[var.name] = 1

        return hidden

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

        config = get_zopeskel_prefs()
        # pastescript allows one to request more than one template (multiple
        # -t options at the command line) so we will get a list of templates
        # from the cmd's options property
        requested_templates = cmd.options.templates

        for var in expect_vars:
            if var.name not in unused_vars:
                for template in requested_templates:
                    if config.has_option(template, var.name):
                        var.default = config.get(template, var.name)
                        break
                if cmd.interactive:
                    prompt = var.pretty_description()
                    response = None
                    while response is None:
                        response = cmd.challenge(prompt, var.default, var.should_echo)
                        if response == '?':
                            print var.further_help()
                            response = None;
                    converted_vars[var.name] = response
                elif var.default is command.NoDefault:
                    errors.append('Required variable missing: %s'
                                  % var.full_description())
                else:
                    converted_vars[var.name] = var.default
            else:
                converted_vars[var.name] = unused_vars.pop(var.name)

            # filter the vars for mode.
            if var.name == 'expert_mode':
                expert_mode = converted_vars['expert_mode']
                hidden = self._filter_for_modes(expert_mode, expect_vars)
                unused_vars.update(hidden)


        if errors:
            raise command.BadCommand(
                'Errors in variables:\n%s' % '\n'.join(errors))
        converted_vars.update(unused_vars)
        vars.update(converted_vars)

        result = converted_vars

        #package = vars["project"]
        #result['namespace_package'], result['package'] = package.split(".")

        return result

    @property
    def pages(self):
        pages = []
        page_map = {}
        for question in self.vars:
            name = question.page
            if name in page_map:
                page = page_map[name]
                page['vars'].append(question)
            else:
                page = {'name': name, 'vars': [question]}
                pages.append(page)
                page_map[name] = page
        return pages
