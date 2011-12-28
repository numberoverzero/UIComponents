import unittest
import Util.Structs as Structs

class EnumTest(unittest.TestCase):
    pass

class TypeCheckedListTest(unittest.TestCase):
    pass

class TypedDoubleBufferTest(unittest.TestCase):
    pass

class TypedLockableListTest(unittest.TestCase):
    pass

def suite():
    test_suite = unittest.TestSuite()
    suite1 = unittest.makeSuite(EnumTest)
    suite2 = unittest.makeSuite(TypeCheckedListTest)
    suite3 = unittest.makeSuite(TypedDoubleBufferTest)
    suite4 = unittest.makeSuite(TypedLockableListTest)
    test_suite.addTests([suite1, suite2, suite3, suite4])
    return test_suite
    
def load_tests():
    return suite()