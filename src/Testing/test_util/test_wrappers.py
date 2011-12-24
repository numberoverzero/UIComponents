import unittest
import Util.Wrappers as Wrappers

class OnChangeTest(unittest.TestCase):
    pass

class InjectArgsTest(unittest.TestCase):
    pass

def suite():
    test_suite = unittest.TestSuite()
    suite1 = unittest.makeSuite(OnChangeTest)
    suite2 = unittest.makeSuite(InjectArgsTest)
    test_suite.addTests([suite1, suite2])
    return test_suite
    
def load_tests():
    return suite()