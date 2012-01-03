import unittest
import Engine.Events as Events

class EventArgsTest(unittest.TestCase):
    def test_constructor(self):
        pass
    
    def test_noneargs(self):
        pass
    
    def test_equality(self):
        pass
    
    def test_str(self):
        pass
    
class EventHandlerTest(unittest.TestCase):
    def test_constructor(self):
        pass
    
    def test_add_handler(self):
        pass
    
    def test_remove_handler(self):
        pass
    
    def test_invoke_empty(self):
        pass
    
    def test_invoke_withargs(self):
        pass
    
    def test_invoke_on_none(self):
        pass
    
    def test_del(self):
        pass
    
def suite():
    test_suite = unittest.TestSuite()
    suite1 = unittest.makeSuite(EventArgsTest)
    suite2 = unittest.makeSuite(EventHandlerTest)
    test_suite.addTests([suite1, suite2])
    return test_suite
    
def load_tests():
    return suite()