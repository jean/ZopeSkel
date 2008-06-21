# -*- coding: utf-8 -*-
"""
Grabs the tests in doctest
"""
__docformat__ = 'restructuredtext'

import unittest
import doctest
import sys
import os
import shutil
import popen2
import tempfile

from zope.testing import doctest

current_dir = os.path.abspath(os.path.dirname(__file__))

def rmdir(*args):
    dirname = os.path.join(*args)
    if os.path.isdir(dirname):
        shutil.rmtree(dirname)

def paster(cmd):
    print "paster %s" % cmd
    from paste.script import command
    #the overwite option for the create command defaults to True
    #but in the paste.script.command it defaults to False.
    #so we fixe it here
    if 'create' in cmd:
        cmd += " --overwrite=True"
    args = cmd.split()
    options, args = command.parser.parse_args(args)
    options.base_parser = command.parser
    command.system_plugins.extend(options.plugins or [])
    commands = command.get_commands()
    command_name = args[0]
    if command_name not in commands:
        command = command.NotFoundCommand
    else:
        command = commands[command_name].load()
    runner = command(command_name)
    runner.run(args[1:])

def read_sh(cmd):
    _cmd = cmd
    old = sys.stdout 
    child_stdout_and_stderr, child_stdin = popen2.popen4(_cmd)
    child_stdin.close()
    return child_stdout_and_stderr.read()

def ls(*args):
    dirname = os.path.join(*args)
    if os.path.isdir(dirname):
        filenames = os.listdir(dirname)
        for filename in sorted(filenames):
            print filename
    else:
        print 'No directory named %s' % dirname

def cd(*args):
    dirname = os.path.join(*args)
    os.chdir(dirname)


def config(filename):
    return os.path.join(current_dir, filename)

def cat(*args):
    filename = os.path.join(*args)
    if os.path.isfile(filename):
        print open(filename).read()
    else:
        print 'No file named %s' % filename

def touch(*args, **kwargs):
    filename = os.path.join(*args)
    open(filename, 'w').write(kwargs.get('data',''))

execdir = os.path.abspath(os.path.dirname(sys.executable))


temp_dirs = []

def get_tempdir():
    tmp_dir = tempfile.mkdtemp()
    temp_dirs.append(tmp_dir)
    return tmp_dir

def tearDown(context):
    for dir_ in temp_dirs:
        shutil.rmtree(dir_, ignore_errors=True)
    temp_dirs[:] = []

def doc_suite(test_dir, setUp=None, tearDown=tearDown, globs=None):
    """Returns a test suite, based on doctests found in /doctest."""
    suite = []
    if globs is None:
        globs = globals()

    flags = (doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE |
             doctest.REPORT_ONLY_FIRST_FAILURE)

    package_dir = os.path.split(test_dir)[0]
    if package_dir not in sys.path:
        sys.path.append(package_dir)

    doctest_dir = os.path.join(package_dir, 'docs')

    # filtering files on extension
    docs = [os.path.join(doctest_dir, doc) for doc in
            os.listdir(doctest_dir) if doc.endswith('.txt')]

    for test in docs:
        suite.append(doctest.DocFileSuite(test, optionflags=flags, 
                                          globs=globs, setUp=setUp, 
                                          tearDown=tearDown,
                                          module_relative=False))

    return unittest.TestSuite(suite)

def test_suite():
    """returns the test suite"""
    return doc_suite(current_dir)

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')

