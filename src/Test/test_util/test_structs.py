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
        #Test wrong type push
        tdb = Structs.TypedDoubleBuffer(int)
        with self.assertRaises(TypeError):
            tdb.push("yellow")
        
        #Test proper push
        tdb.push(3)
        tbd_fb = tdb.get_front_buffer_items()
        tbd_bb = tdb.get_back_buffer_items()
        expected_fb = 0
        expected_bb = 1
        actual_fb = len(tbd_fb)
        actual_bb = len(tbd_bb)
        self.assertTrue(expected_fb == actual_fb)
        self.assertTrue(expected_bb == actual_bb)
    
    def test_pop(self):
        #Test that pop from empty list raises IndexError
        tdb = Structs.TypedDoubleBuffer(int)
        with self.assertRaises(IndexError):
            tdb.pop()
        
        #Test that pop after push STILL raises IndexError since push is to bbuf
        tdb = Structs.TypedDoubleBuffer(int)
        tdb.push(3)
        with self.assertRaises(IndexError):
            tdb.pop()
        
        #Test that pop after push AND flip correctly gets the item back
            #Push an item after the flip to make sure that item doesn't get returned
                #(should be in back buffer)
        tdb = Structs.TypedDoubleBuffer(str)
        tdb.push("Yellow")
        tdb.flip(mode = 'exact')
        tdb.push("Red")
        expected = "Yellow"
        actual = tdb.pop()
        self.assertTrue(expected == actual)
        with self.assertRaises(IndexError):
            tdb.pop()
    
    def test_clear(self):
        #Test clear on front only
        tdb = Structs.TypedDoubleBuffer(int)
        tdb.push(3)
        tdb.push(4)
        tdb.flip(mode='exact')
        tdb.push(100)
        tdb.push(200)
        tdb.clear(front = True, back = False)
        
        expected_front = []
        actual_front = tdb.get_front_buffer_items()
        self.assertListEqual(expected_front, actual_front)
        expected_back = [100,200]
        actual_back = tdb.get_back_buffer_items()
        self.assertListEqual(expected_back, actual_back)
        
        #Test clear on back only
        tdb = Structs.TypedDoubleBuffer(int)
        tdb.push(3)
        tdb.push(4)
        tdb.flip(mode='exact')
        tdb.push(100)
        tdb.push(200)
        tdb.clear(front = False, back = True)
        
        expected_front = [3,4]
        actual_front = tdb.get_front_buffer_items()
        self.assertListEqual(expected_front, actual_front)
        expected_back = []
        actual_back = tdb.get_back_buffer_items()
        self.assertListEqual(expected_back, actual_back)
        
        #Test clear on both
        tdb = Structs.TypedDoubleBuffer(int)
        tdb.push(3)
        tdb.push(4)
        tdb.flip(mode='exact')
        tdb.push(100)
        tdb.push(200)
        tdb.clear(front = True, back = True)
        
        expected_front = []
        actual_front = tdb.get_front_buffer_items()
        self.assertListEqual(expected_front, actual_front)
        expected_back = []
        actual_back = tdb.get_back_buffer_items()
        self.assertListEqual(expected_back, actual_back)
        
        #Test clear on neither
        tdb = Structs.TypedDoubleBuffer(int)
        tdb.push(3)
        tdb.push(4)
        tdb.flip(mode='exact')
        tdb.push(100)
        tdb.push(200)
        tdb.clear(front = False, back = False)
        
        expected_front = [3,4]
        actual_front = tdb.get_front_buffer_items()
        self.assertListEqual(expected_front, actual_front)
        expected_back = [100,200]
        actual_back = tdb.get_back_buffer_items()
        self.assertListEqual(expected_back, actual_back)
        
    def test_flip_exact(self):
        tdb = Structs.TypedDoubleBuffer(int)
        tdb.push(3)
        tdb.push(4)
        tdb.flip(mode='exact')
        tdb.push(100)
        tdb.push(200)
        tdb.flip(mode='exact')
        
        expected_front = [100, 200]
        actual_front = tdb.get_front_buffer_items()
        self.assertListEqual(expected_front, actual_front)
        expected_back = [3, 4]
        actual_back = tdb.get_back_buffer_items()
        self.assertListEqual(expected_back, actual_back)
    
    def test_flip_transfer(self):
        tdb = Structs.TypedDoubleBuffer(int)
        tdb.push(3)
        tdb.push(4)
        tdb.flip(mode='exact') #This flip is simply so that we can put stuff
                                #In both buffers
        tdb.push(100)
        tdb.push(200)
        
        tdb.flip(mode='transfer') #This is the flip we're testing
        
        expected_front = [3, 4, 100, 200]
        actual_front = tdb.get_front_buffer_items()
        self.assertListEqual(expected_front, actual_front)
        expected_back = []
        actual_back = tdb.get_back_buffer_items()
        self.assertListEqual(expected_back, actual_back)
    
    def test_flip_discard(self):
        tdb = Structs.TypedDoubleBuffer(int)
        tdb.push(3)
        tdb.push(4)
        tdb.flip(mode='exact') #This flip is simply so that we can put stuff
                                #In both buffers
        tdb.push(100)
        tdb.push(200)
        
        tdb.flip(mode='discard') #This is the flip we're testing
        
        expected_front = [100, 200]
        actual_front = tdb.get_front_buffer_items()
        self.assertListEqual(expected_front, actual_front)
        expected_back = []
        actual_back = tdb.get_back_buffer_items()
        self.assertListEqual(expected_back, actual_back)
    
    def test_flip_transfer_front(self):
        tdb = Structs.TypedDoubleBuffer(int)
        tdb.push(3)
        tdb.push(4)
        tdb.flip(mode='exact') #This flip is simply so that we can put stuff
                                #In both buffers
        tdb.push(100)
        tdb.push(200)
        
        tdb.flip(mode='transfer_front') #This is the flip we're testing
        
        expected_front = [100, 200, 3, 4]
        actual_front = tdb.get_front_buffer_items()
        self.assertListEqual(expected_front, actual_front)
        expected_back = []
        actual_back = tdb.get_back_buffer_items()
        self.assertListEqual(expected_back, actual_back)

class TypedLockableListTest(unittest.TestCase):
    def test_init(self):
        #Test empty constructor
        empty_tcl = Structs.TypedLockableList(int, items = None,
                                            suppress_type_errors = True)
        actual = len(empty_tcl)
        expected = 0
        self.assertTrue(actual == expected)
        
        #Test constructor with items
        items = [1,2,3,'bob']
        tcl = Structs.TypedLockableList(int, items = items,
                                      suppress_type_errors = True)
        actual = len(tcl)
        expected = 3
        self.assertTrue(actual == expected)
        
        #Test bad extend with no TypeError suppression
        items = [1,2,3,'bob']
        with self.assertRaises(TypeError):
            tcl = Structs.TypedLockableList(int, items = items,
                                          suppress_type_errors = False)
            
    def test_append(self):
        #Test append on unlocked
        
        #Test append of wrong type with no suppression
        
        #Test append on locked- check _to_add and len()
        
        pass
    
    def test_extend(self):
        #Test extend on unlocked
        
        #Test extend of wrong type with no suppression
        
        #Test extend on locked- check _to_add and len()
        
        pass
    
    def test_remove(self):
        #Test remove on unlocked with item in set
        
        #Test remove on unlocked with item (wrong type) NOT in set
        
        #Test remove of existing item on locked- check _to_add and len()
        
        pass
    
    def test_lock(self):
        pass
    
    def test_call(self):
        pass
    
    def test_sort(self):
        pass
    
    def test_properties(self):
        #Check HasPendingUpdates, IsLocked
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