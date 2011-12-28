import unittest
import Util.Structs as Structs

class EnumTest(unittest.TestCase):
    def test_empty_enum(self):
        empty_enum = Structs.enum()
        actual = type(empty_enum) == type
        self.assertTrue(actual)
        
    def test_no_key(self):
        an_enum = Structs.enum("bob","steve")
        with self.assertRaises(AttributeError):
            actual = an_enum.jim
            
    def test_valid_key(self):
        an_enum = Structs.enum("bob","steve")
        actual = an_enum.steve
        expected = 1
        self.assertTrue(actual==expected)

class TypeCheckedListTest(unittest.TestCase):
    def test_init(self):
        #Test empty constructor
        empty_tcl = Structs.TypeCheckedList(int, items = None,
                                            suppress_type_errors = True)
        actual = len(empty_tcl)
        expected = 0
        self.assertTrue(actual == expected)
        
        #Test constructor with items
        items = [1,2,3,'bob']
        tcl = Structs.TypeCheckedList(int, items = items,
                                      suppress_type_errors = True)
        actual = len(tcl)
        expected = 3
        self.assertTrue(actual == expected)
        
        #Test bad extend with no TypeError suppression
        items = [1,2,3,'bob']
        with self.assertRaises(TypeError):
            tcl = Structs.TypeCheckedList(int, items = items,
                                          suppress_type_errors = False)
    
    def test_append(self):
        #Test appending good item
        items = ["bob", "steve"]
        tcl = Structs.TypeCheckedList(str, items = items,
                                      suppress_type_errors = True)
        tcl.append("jack")
        actual = len(tcl)
        expected = 3
        self.assertTrue(actual == expected)
        
        #Test appending bad item, suppression on
        items = ["bob", "steve"]
        tcl = Structs.TypeCheckedList(str, items = items,
                                      suppress_type_errors = True)
        tcl.append(3)
        actual = len(tcl)
        expected = 2
        self.assertTrue(actual == expected)
        
        #Test appending bad item, suppression off
        items = ["bob", "steve"]
        tcl = Structs.TypeCheckedList(str, items = items,
                                      suppress_type_errors = False)
        with self.assertRaises(TypeError):
            tcl.append(3)
        
    
    def test_extend(self):
        #Test extend with empty iterable
        items = ["bob", "steve"]
        tcl = Structs.TypeCheckedList(str, items = items,
                                      suppress_type_errors = True)
        tcl.extend([])
        actual = len(tcl)
        expected = 2
        self.assertTrue(actual == expected)
        
        #Test extend with a non-iterable
        items = ["bob", "steve"]
        tcl = Structs.TypeCheckedList(str, items = items,
                                      suppress_type_errors = True)
        tcl.extend("jack")
        actual = len(tcl)
        expected = 3
        self.assertTrue(actual == expected)
        
        #Test extend with all valid
        items = ["bob", "steve"]
        tcl = Structs.TypeCheckedList(str, items = items,
                                      suppress_type_errors = True)
        tcl.extend(items)
        actual = len(tcl)
        expected = 4
        self.assertTrue(actual == expected)
        
        #Test extend with some invalid, suppressed
        items = ["bob", "steve"]
        tcl = Structs.TypeCheckedList(str, items = items,
                                      suppress_type_errors = True)
        tcl.extend(["jack", 3])
        actual = len(tcl)
        expected = 3
        self.assertTrue(actual == expected)
        
        #Test extend with some invalid, not suppressed
        items = ["bob", "steve"]
        tcl = Structs.TypeCheckedList(str, items = items,
                                      suppress_type_errors = False)
        with self.assertRaises(TypeError):
            tcl.extend(["jack",3])
    
    def test_clear(self):
        items = ["bob", "steve"]
        tcl = Structs.TypeCheckedList(str, items = items,
                                      suppress_type_errors = True)
        tcl.append("jack")
        actual = len(tcl)
        expected = 3
        self.assertTrue(actual == expected)
        
        tcl.clear()
        actual = len(tcl)
        expected = 0
        self.assertTrue(actual == expected)
        

class TypedDoubleBufferTest(unittest.TestCase):
    def test_push(self):
        pass
    
    def test_pop(self):
        pass
    
    def test_clear(self):
        pass
    
    def test_flip_transfer(self):
        pass
    
    def test_flip_discard(self):
        pass
    
    def test_flip_transfer_front(self):
        pass

class TypedLockableListTest(unittest.TestCase):
    def test_init(self):
        pass
    
    def test_append(self):
        pass
    
    def test_extend(self):
        pass
    
    def test_remove(self):
        pass
    
    def test_lock(self):
        pass
    
    def test_call(self):
        pass
    
    def test_sort(self):
        pass
    
    def test_properties(self):
        #Check HasPendingUpdates, Islocked
        pass
    
    def test_clear_change_flag(self):
        pass
    
    def test_clear(self):
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