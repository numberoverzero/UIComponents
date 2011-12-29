import unittest
import Util.Wrappers as Wrappers

class OnChangeTest(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        class tst_class(object):
            flag = False
            _x = 0
            def _g_x(self):
                return self._x
            @Wrappers.on_change('x', 'flag')
            def _s_x(self, value):
                self._x = value
            x = property(_g_x, _s_x)
            
        self.tst_cls = tst_class
    
    def test_no_change(self):
        bob = self.tst_cls()
        self.assertFalse(bob.flag)
        bob.x = 0
        self.assertFalse(bob.flag)
    
    def test_change(self):
        bob = self.tst_cls()
        self.assertFalse(bob.flag)
        bob.x = 1
        self.assertTrue(bob.flag)
        
    def test_flag_auto_clear(self):
        """The flag should never be set to false by the wrapper-
            it must be explicitly dealt with by the class.
            This test should show that the flag remains true even when
            given the same value."""
        bob = self.tst_cls()
        self.assertFalse(bob.flag)
        bob.x = 1
        self.assertTrue(bob.flag)
        bob.x = 1
        self.assertTrue(bob.flag)

class InjectArgsTest(unittest.TestCase):
    #Test out of order args
    
    #Test no default args
    
    #Test no args
    
    #Test not using kwargs raises error
    
    #Test all default args
    
    #Test mixing arg/kwarg order
    
    #Test ignore on all args
    
    #Test ignore on middle kwarg
    
    #Test ignore on last kwarg
    
    #Test ignore on non-kwarg
    pass

def suite():
    test_suite = unittest.TestSuite()
    suite1 = unittest.makeSuite(OnChangeTest)
    suite2 = unittest.makeSuite(InjectArgsTest)
    test_suite.addTests([suite1, suite2])
    return test_suite
    
def load_tests():
    return suite()