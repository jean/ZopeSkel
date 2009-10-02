# -*- coding: utf-8 -*-

import unittest

from zopeskel.base import var, BooleanVar, StringVar, TextVar, DottedVar
from zopeskel.base import ValidationException

class test_var(unittest.TestCase):
    """ test that there is no default implementation of the validation method
    """
    def setUp(self):
        self.var = var('name', 'description')
    
    def testValidation(self):
        """ the validation method should raise a ValidationException
        """
        try:
            self.var.validate('foo')
        except NotImplementedError:
            pass
        else:
            self.fail("The validation method should not be implemented on the basic var class")


class test_BooleanVar(unittest.TestCase):
    """ verify functionality of the BooleanVar variable class
    """
    def setUp(self):
        self.bvar = BooleanVar('name', 'description')
    
    def testValidation(self):
        """ check to see that various inputs result in a Boolean Value
        """
        self.failIf(self.bvar.validate('f'))
        self.failIf(self.bvar.validate('F'))
        self.failIf(self.bvar.validate('n'))
        self.failIf(self.bvar.validate('N'))
        self.failIf(self.bvar.validate('false'))
        self.failIf(self.bvar.validate(0))
        
        self.failUnless(self.bvar.validate('t'))
        self.failUnless(self.bvar.validate('T'))
        self.failUnless(self.bvar.validate('y'))
        self.failUnless(self.bvar.validate('Y'))
        self.failUnless(self.bvar.validate('true'))
        self.failUnless(self.bvar.validate(1))
        
        self.assertRaises(ValidationException, self.bvar.validate, 'humpty-dumpty')


class test_StringVar(unittest.TestCase):
    """ verify functionality of the StringVar variable class
    """
    def setUp(self):
        self.svar = StringVar('name', 'description')
    
    def testValidation(self):
        """ check to see that validation returns appropriate values:
                string should have no spaces at front or back
                unicode strings and regular strings should pass through unchanged
                non-string values raise validation errors
        """
        val = 'george'
        self.assertEqual(val, self.svar.validate(val))
        
        val = u'george'
        self.assertEqual(val, self.svar.validate(val))
        
        val = ' hello '
        validated = self.svar.validate(val)
        self.assertNotEqual(validated[0], ' ')
        self.assertNotEqual(validated[-1], ' ')
        self.failUnless(validated in val)
        
        for val in (0, True):
            self.assertRaises(ValidationException, self.svar.validate, val)


class test_TextVar(unittest.TestCase):
    """ verify functionality of the TextVar variable class
    """
    def setUp(self):
        self.tvar = TextVar('name', 'description')
    
    def testValidation(self):
        """ we will test this more thoroughly when it does something useful that
            is different than the above.
        """
        pass


class test_DottedVar(unittest.TestCase):
    def setUp(self):
        self.dvar = DottedVar('name', 'description')
    
    def testValidation(self):
        """ all parts of a dotted name must be valid python identifiers
        """
        for val in ('this.package', '_foo_.bar', '__class__.__name__'):
            self.assertEquals(val, self.dvar.validate(val))
        
        for val in ('ham-and-eggs.yummy', 'spam.yucky!'):
            self.assertRaises(ValidationException, self.dvar.validate, val)


def test_suite():
    suite = unittest.TestSuite([
        unittest.makeSuite(test_var),
        unittest.makeSuite(test_BooleanVar),
        unittest.makeSuite(test_StringVar),
        unittest.makeSuite(test_TextVar),
        unittest.makeSuite(test_DottedVar),
    ])
    return suite
    
if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')