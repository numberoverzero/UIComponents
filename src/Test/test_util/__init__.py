"""
Tests the util module
"""

import unittest
import Util

class UtilTest(unittest.TestCase):
    def test_class_name(self):
        class a_test(object):
            pass
        class _(object):
            pass
        
        cname = Util.class_name(a_test())
        expected = "Test.test_util.a_test"
        self.assertEqual(cname, expected)
        
        cname = Util.class_name(_())
        expected = "Test.test_util._"
        self.assertEqual(cname, expected)
        
    
    def test_ensure_type(self):
        #test same type already
        a = [1, 2, 3]
        a_int = Util.ensure_type(a, int)
        self.assertListEqual(a_int, [1, 2, 3])
        
        #test all wrong
        a = ['1', '2', '3']
        a_int = Util.ensure_type(a, int)
        self.assertListEqual(a_int, [1, 2, 3])
        
        #test mixed
        a = ['1', 2, '3']
        a_int = Util.ensure_type(a, int)
        self.assertListEqual(a_int, [1, 2, 3])
        
        #test empty
        a = []
        a_int = Util.ensure_type(a, int)
        self.assertListEqual(a_int, [])

def suite():
    suite1 = unittest.makeSuite(UtilTest)
    return suite1
    
def load_tests():
    return suite()