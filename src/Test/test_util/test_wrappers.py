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
    def setUp(self):
        unittest.TestCase.setUp(self)
        class obj(object):
            pass
        self.obj = obj
    
    def test_no_args_or_kwargs(self):
        #1) Empty ignores
        obj = self.obj()
        @Wrappers.inject_args(ignores = None)
        def fn_1(self):
            self.x = 'default'
        self.obj.fn_1 = fn_1

            #Test that x is found
        obj.fn_1()
        actual = obj.x
        expected = "default"
        self.assertEqual(actual, expected)    
        
            #Test that a passed x value is not used
        with self.assertRaises(TypeError):
            obj.fn_1(x = 'not_default')
            actual = obj.x
            expected = "default"
            self.assertEqual(actual, expected)
        
            #Test that a passed y is not injected
        with self.assertRaises(TypeError):
            obj.fn_1(y = 'this is bad')
            print obj.y
        
        #2) Ignores x
        obj = self.obj()
        @Wrappers.inject_args(ignores = ['x'])
        def fn_2(self):
            self.x = 'default'
        self.obj.fn_2 = fn_2

            #Test that x is found
        obj.fn_2()
        actual = obj.x
        expected = "default"
        self.assertEqual(actual, expected)    
        
            #Test that a passed x value is not used
        with self.assertRaises(TypeError):
            obj.fn_2(x = 'not_default')
            actual = obj.x
            expected = "default"
            self.assertEqual(actual, expected)
            
            #Test that a passed y is not injected
        with self.assertRaises(TypeError):
            obj.fn_2(y = 'this is bad')
            print obj.y
            
        #3) Ignores y
        obj = self.obj()
        @Wrappers.inject_args(ignores = ['y'])
        def fn_3(self):
            self.x = 'default'
        self.obj.fn_3 = fn_3
        
            #Test that x is found
        obj.fn_3()
        actual = obj.x
        expected = "default"
        self.assertEqual(actual, expected)    
        
            #Test that a passed x value is not used
        with self.assertRaises(TypeError):
            obj.fn_3(x = 'not_default')
            actual = obj.x
            expected = "default"
            self.assertEqual(actual, expected)
                
            #Test that a passed y is not injected
        with self.assertRaises(TypeError):
            obj.fn_3(y = 'this is bad')
            print obj.y
            
        #Delete the functions
        del(self.obj.fn_1)
        del(self.obj.fn_2)
        del(self.obj.fn_3)
        
    def test_only_args_empty_ignores(self):
        """Position args only, nothing ignored."""
        obj = self.obj()
        @Wrappers.inject_args(ignores = None)
        def fn(self, x, y, n):
            self.x = 'default'
        self.obj.fn = fn

            #Test that x takes fn body value, y and n get picked up
        obj.fn(x = 'not default', y = -1, n = 3)
        actual = [obj.x, obj.y, obj.n]
        expected = ["default", -1, 3]
        self.assertListEqual(actual, expected)
        
            #Test that a passed z value is not injected
        with self.assertRaises(TypeError):
            obj.fn(x = 'not default', y = -1, n = 3, z = 'not_default')
        
            #Test that too few args raises error
        with self.assertRaises(TypeError):
            obj.fn(x = 'not_default', y = 'this is bad')
            
        #Delete the function
        del(self.obj.fn)

    def test_only_args_included_ignores(self):
        """Position args only, one position arg ignores."""
        obj = self.obj()
        @Wrappers.inject_args(ignores = ['y'])
        def fn(self, x, y, n):
            self.x = 'default'
        self.obj.fn = fn

            #Test that x takes fn body value, n gets picked up (NOT y)
        obj.fn(x = 'not_default', y = -1, n = 3)
        actual = [obj.x, obj.n]
        expected = ["default", 3]
        self.assertListEqual(actual, expected)
            #Test that the y value wasn't injected in
        with self.assertRaises(AttributeError):
            obj.y
        
            #Test that a passed z value is not injected
        with self.assertRaises(TypeError):
            obj.fn(x = 'not default', y = -1, n = 3, z = 'not_default')
        
            #Test that too few args raises error
        with self.assertRaises(TypeError):
            obj.fn(x = 'not default', y = 'this is bad')
        
        #Delete the function
        del(self.obj.fn)

    def test_only_args_non_included_ignores(self):
        """Position args only, a variable not in args is ignored."""
        obj = self.obj()
        @Wrappers.inject_args(ignores = ['z'])
        def fn(self, x, y, n):
            self.x = 'default'
        self.obj.fn = fn
        
            #Test that x takes fn body value, y and n get picked up
        obj.fn(x = 'not_default', y = -1, n = 3)
        actual = [obj.x, obj.y, obj.n]
        expected = ["default", -1, 3]
        self.assertListEqual(actual, expected)
        
            #Test that a passed z value is not injected
        with self.assertRaises(TypeError):
            obj.fn(z = 'not_default')
        
            #Test that too few args raises error
        with self.assertRaises(TypeError):
            obj.fn(x = 'not_default', y = 'this is bad')
        
        #Delete the function
        del(self.obj.fn)
        
    def test_only_kwargs_empty_ignores(self):
        """Keyword args only, nothing ignored."""
        pass
    
    def test_only_kwargs_included_ignores(self):
        """Keyword args only, one kwarg ignores."""
        pass
    
    def test_only_kwargs_non_included_ignores(self):
        """Keyword args only, a var not in kwargs is ignored."""
        pass
    
    def test_args_and_kwargs_empty_ignores(self):
        """Args and kwargs, nothing ignored."""
        pass
    
    def test_args_and_kwargs_included_ignores(self):
        """Args and kwargs, one kwarg ignores."""
        pass
    
    def test_args_and_kwargs_non_included_ignores(self):
        """Args and kwargs, a var not in kwargs is ignored."""
        pass


def suite():
    test_suite = unittest.TestSuite()
    suite1 = unittest.makeSuite(OnChangeTest)
    suite2 = unittest.makeSuite(InjectArgsTest)
    test_suite.addTests([suite1, suite2])
    return test_suite
    
def load_tests():
    return suite()