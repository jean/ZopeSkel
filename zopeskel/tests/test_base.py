# -*- coding: utf-8 -*-

import unittest

from zopeskel.base import BaseTemplate, get_var
from zopeskel.vars import var, BooleanVar, StringVar, TextVar, DottedVar
from zopeskel.vars import EXPERT, EASY

class test_base_template(unittest.TestCase):
    """ test for methods on the base template class
    """
    def setUp(self):
        """ set up some basics for the coming tests
        """
        self.vars = [
            var('basic_var', 'This is a basic variable', 
                title="Basic Title", default="foo",
                modes=(EXPERT, EASY)),
            BooleanVar('bool_var', 'This is a boolean variable',
                       title="Boolean Title", default=False,
                       modes=(EASY)),
            StringVar('str_var', 'This is a string variable',
                      title="String Title", default="string",
                      modes=(EXPERT)),
            TextVar('txt_var', 'This is a text variable',
                    title="Text Title", default="text",
                    modes=()),
            DottedVar('dot_var', 'This is a dotted variable',
                      title="Dotted Title", default="dotted.variable")
        ]
        self.template = BaseTemplate('my_name')
    
    def test_filter_for_modes(self):
        """ _filter_for_modes should return a dictionary of var names to 
            be hidden from view dependant on the running mode of zopeskel
            and the modes property of each variable
        """
        easy_vars = [var.name for var in self.vars 
                     if EASY not in var.modes]
        expert_vars = [var.name for var in self.vars 
                       if EXPERT not in var.modes]
        
        expert_mode = False
        hidden = self.template._filter_for_modes(expert_mode, self.vars)
        
        self.assertEqual(len(hidden), 2)
        for varname in hidden.keys():
            self.failUnless(varname in easy_vars, 
                            "missing easy var: %s" % varname)
            
        expert_mode = True
        hidden = self.template._filter_for_modes(expert_mode, self.vars)
        
        self.assertEqual(len(hidden), 2)
        for varname in hidden.keys():
            self.failUnless(varname in expert_vars, 
                            "missing expert var: %s" % varname)
    
    def test_get_vars(self):
        """ get_vars is not a method of BaseTemplate, but we've got a nice set
            of variables all set up in here, so let's use it
        """
        var = get_var(self.vars, 'basic_var')
        self.assertEqual(var.name, 'basic_var')
        self.assertEqual(var.title, 'Basic Title')
        self.assertEqual(var.description, 'This is a basic variable')
        self.assertEqual(var.modes, (EXPERT, EASY))
        self.assertEqual(var.default, 'foo')


def test_suite():
    suite = unittest.TestSuite([
        unittest.makeSuite(test_base_template),
    ])
    return suite
    
if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')