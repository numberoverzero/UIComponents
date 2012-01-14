import unittest
import Util.Structs as Structs

class EnumTest(unittest.TestCase):
    def test_empty_enum(self):
        empty_enum = Structs.enum()
        actual = type(empty_enum) == type
        self.assertTrue(actual)
        
    def test_no_key(self):
        an_enum = Structs.enum("bob", "steve")
        with self.assertRaises(AttributeError):
            an_enum.jim
            
    def test_valid_key(self):
        an_enum = Structs.enum("bob", "steve")
        actual = an_enum.steve
        expected = 1
        self.assertTrue(actual == expected)

class TypeCheckedListTest(unittest.TestCase):
    def test_init(self):
        #Test empty constructor
        empty_tcl = Structs.TypeCheckedList(int, values=None,
                                            suppress_type_errors=True)
        actual = len(empty_tcl)
        expected = 0
        self.assertTrue(actual == expected)
        
        #Test constructor with values
        values = [1, 2, 3, 'bob']
        tcl = Structs.TypeCheckedList(int, values=values,
                                      suppress_type_errors=True)
        actual = len(tcl)
        expected = 3
        self.assertTrue(actual == expected)
        
        #Test bad extend with no TypeError suppression
        values = [1, 2, 3, 'bob']
        with self.assertRaises(TypeError):
            tcl = Structs.TypeCheckedList(int, values=values,
                                          suppress_type_errors=False)
    
    def test_append(self):
        #Test appending good value
        values = ["bob", "steve"]
        tcl = Structs.TypeCheckedList(str, values=values,
                                      suppress_type_errors=True)
        tcl.append("jack")
        actual = len(tcl)
        expected = 3
        self.assertTrue(actual == expected)
        
        #Test appending bad value, suppression on
        values = ["bob", "steve"]
        tcl = Structs.TypeCheckedList(str, values=values,
                                      suppress_type_errors=True)
        tcl.append(3)
        actual = len(tcl)
        expected = 2
        self.assertTrue(actual == expected)
        
        #Test appending bad value, suppression off
        values = ["bob", "steve"]
        tcl = Structs.TypeCheckedList(str, values=values,
                                      suppress_type_errors=False)
        with self.assertRaises(TypeError):
            tcl.append(3)
        
    
    def test_extend(self):
        #Test extend with empty iterable
        values = ["bob", "steve"]
        tcl = Structs.TypeCheckedList(str, values=values,
                                      suppress_type_errors=True)
        tcl.extend([])
        actual = len(tcl)
        expected = 2
        self.assertTrue(actual == expected)
        
        #Test extend with a non-iterable
        values = ["bob", "steve"]
        tcl = Structs.TypeCheckedList(str, values=values,
                                      suppress_type_errors=True)
        tcl.extend("jack")
        actual = len(tcl)
        expected = 3
        self.assertTrue(actual == expected)
        
        #Test extend with all valid
        values = ["bob", "steve"]
        tcl = Structs.TypeCheckedList(str, values=values,
                                      suppress_type_errors=True)
        tcl.extend(values)
        actual = len(tcl)
        expected = 4
        self.assertTrue(actual == expected)
        
        #Test extend with some invalid, suppressed
        values = ["bob", "steve"]
        tcl = Structs.TypeCheckedList(str, values=values,
                                      suppress_type_errors=True)
        tcl.extend(["jack", 3])
        actual = len(tcl)
        expected = 3
        self.assertTrue(actual == expected)
        
        #Test extend with some invalid, not suppressed
        values = ["bob", "steve"]
        tcl = Structs.TypeCheckedList(str, values=values,
                                      suppress_type_errors=False)
        with self.assertRaises(TypeError):
            tcl.extend(["jack", 3])
    
    def test_clear(self):
        values = ["bob", "steve"]
        tcl = Structs.TypeCheckedList(str, values=values,
                                      suppress_type_errors=True)
        tcl.append("jack")
        actual = len(tcl)
        expected = 3
        self.assertTrue(actual == expected)
        
        tcl.clear()
        actual = len(tcl)
        expected = 0
        self.assertTrue(actual == expected)

class DoubleBufferTest(unittest.TestCase):
    def test_push(self):
        #Test wrong type push
        tdb = Structs.DoubleBuffer()
        
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
        tdb = Structs.DoubleBuffer()
        with self.assertRaises(IndexError):
            tdb.pop()
        
        #Test that pop after push STILL raises IndexError since push is to bbuf
        tdb = Structs.DoubleBuffer()
        tdb.push(3)
        with self.assertRaises(IndexError):
            tdb.pop()
        
        #Test that pop after push AND flip correctly gets the value back
            #Push an value after the flip to make sure that value doesn't get returned
                #(should be in back buffer)
        tdb = Structs.DoubleBuffer()
        tdb.push("Yellow")
        tdb.flip(mode='exact')
        tdb.push("Red")
        expected = "Yellow"
        actual = tdb.pop()
        self.assertTrue(expected == actual)
        with self.assertRaises(IndexError):
            tdb.pop()
    
    def test_clear(self):
        #Test clear on front only
        tdb = Structs.DoubleBuffer()
        tdb._write_front_buffer(3)
        tdb._write_front_buffer(4)
        tdb._write_back_buffer(100)
        tdb._write_back_buffer(200)
        tdb.clear(front=True, back=False)
        
        expected_front = []
        actual_front = tdb.get_front_buffer_items()
        self.assertListEqual(expected_front, actual_front)
        expected_back = [100, 200]
        actual_back = tdb.get_back_buffer_items()
        self.assertListEqual(expected_back, actual_back)
        
        #Test clear on back only
        tdb = Structs.DoubleBuffer()
        tdb._write_front_buffer(3)
        tdb._write_front_buffer(4)
        tdb._write_back_buffer(100)
        tdb._write_back_buffer(200)
        tdb.clear(front=False, back=True)
        
        expected_front = [3, 4]
        actual_front = tdb.get_front_buffer_items()
        self.assertListEqual(expected_front, actual_front)
        expected_back = []
        actual_back = tdb.get_back_buffer_items()
        self.assertListEqual(expected_back, actual_back)
        
        #Test clear on both
        tdb = Structs.DoubleBuffer()
        tdb._write_front_buffer(3)
        tdb._write_front_buffer(4)
        tdb._write_back_buffer(100)
        tdb._write_back_buffer(200)
        tdb.clear(front=True, back=True)
        
        expected_front = []
        actual_front = tdb.get_front_buffer_items()
        self.assertListEqual(expected_front, actual_front)
        expected_back = []
        actual_back = tdb.get_back_buffer_items()
        self.assertListEqual(expected_back, actual_back)
        
        #Test clear on neither
        tdb = Structs.DoubleBuffer()
        tdb._write_front_buffer(3)
        tdb._write_front_buffer(4)
        tdb._write_back_buffer(100)
        tdb._write_back_buffer(200)
        tdb.clear(front=False, back=False)
        
        expected_front = [3, 4]
        actual_front = tdb.get_front_buffer_items()
        self.assertListEqual(expected_front, actual_front)
        expected_back = [100, 200]
        actual_back = tdb.get_back_buffer_items()
        self.assertListEqual(expected_back, actual_back)
        
    def test_flip_exact(self):
        tdb = Structs.DoubleBuffer()
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
        tdb = Structs.DoubleBuffer()
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
        tdb = Structs.DoubleBuffer()
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
        tdb = Structs.DoubleBuffer()
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

class LockableListTest(unittest.TestCase):
    def test_init(self):
        #Test empty constructor
        empty_tll = Structs.LockableList(values=None)
        actual = len(empty_tll)
        expected = 0
        self.assertTrue(actual == expected)
        
        #Test constructor with values
        values = [1, 2, 3, 'bob']
        tll = Structs.LockableList(values=values)
        actual = len(tll)
        expected = 4
        self.assertTrue(actual == expected)
            
    def test_append(self):
        #Test append on unlocked
        tll = Structs.LockableList(values=None)
        tll.append("Yellow")
        actual = len(tll)
        expected = 1
        self.assertTrue(actual == expected)
        
        
        #Test append on locked- check _to_add and len()
        tll = Structs.LockableList(values=None)
        tll.lock(set_lock=True, force_update=False)
        tll.append("Yellow")
        
        actual = len(tll._to_add)
        expected = 1
        self.assertTrue(actual == expected)
        
        actual = len(tll)
        expected = 0
        self.assertTrue(actual == expected)
    
    def test_extend(self):
        #Test extend on unlocked
        tll = Structs.LockableList(values=None)
        tll.extend(["Yellow", "Blue"])
        actual = len(tll)
        expected = 2
        self.assertTrue(actual == expected)
                    
        #Test extend on locked- check _to_add and len()
        tll = Structs.LockableList(values=None)
        tll.lock(set_lock=True, force_update=False)
        tll.extend(["Yellow", "Red"])
        
        actual = len(tll._to_add)
        expected = 2
        self.assertTrue(actual == expected)
        
        actual = len(tll)
        expected = 0
        self.assertTrue(actual == expected)
    
    def test_remove(self):
        #Test remove on unlocked with value in set
        tll = Structs.LockableList(values=None)
        tll.extend([3, 4, 5])
        tll.remove(4)
        actual = len(tll)
        expected = 2
        self.assertTrue(actual == expected)
        
        #Test remove on unlocked with value NOT in set
        tll = Structs.LockableList(values=None)
        tll.extend([3, 4, 5])
        with self.assertRaises(ValueError):
            tll.remove(100)
        
        
        #Test remove of existing value on locked- check _to_add and len()
        tll = Structs.LockableList(values=None)
        tll.extend([3, 4, 5])
        tll.lock(set_lock=True, force_update=False)
        tll.remove(4)
        actual = len(tll)
        expected = 3
        self.assertTrue(actual == expected)
    
    def test_lock(self):
        #Test locking an item
        tll = Structs.LockableList(values=None)
        tll.lock(set_lock=True, force_update=False)
        self.assertTrue(tll.IsLocked)
        
        #Test unlocking an item with update
        tll = Structs.LockableList(values=None)
        tll.extend([3, 4, 5])
        tll.lock(set_lock=True, force_update=False)
        tll.remove(4)
        actual = len(tll)
        expected = 3
        self.assertTrue(actual == expected)
        tll.lock(set_lock=False, force_update=True)
        actual = len(tll)
        expected = 2
        self.assertTrue(actual == expected)
        
        #Test toggle lock
        tll = Structs.LockableList(values=None)
        self.assertTrue(not tll.IsLocked)
        tll.lock()
        self.assertTrue(tll.IsLocked)
        tll.lock()
        self.assertTrue(not tll.IsLocked)
        
    def test_call(self):
        #Test normal behavior
        tll = Structs.LockableList(values=None)
        tll.extend([3, 4, 5])
        actual = []
        expected = [3, 4, 5]
        for value in tll:
            actual.append(value)
        self.assertListEqual(actual, expected)
        
        #Test locked behavior with pending addition
        tll = Structs.LockableList(values=None)
        tll.extend([3, 4, 5])
        tll.lock()
        tll.append(100)
        actual = []
        expected = [3, 4, 5]
        for value in tll:
            actual.append(value)
        self.assertListEqual(actual, expected)
        
        #Make sure the call is applying pending updates
        tll = Structs.LockableList(values=None)
        tll.extend([3, 4, 5])
        tll.lock(force_update=False)
        tll.append(100)
        tll.lock(force_update=False)
        actual = []
        expected = [3, 4, 5, 100]
        for value in tll:
            actual.append(value)
        self.assertListEqual(actual, expected)
    
    def test_sort(self):
        #Test sort for normal behavior
        tll = Structs.LockableList(values=None)
        tll.extend([5, 3, 4])
        tll.sort()
        actual = tll[:]
        expected = [3, 4, 5]
        self.assertListEqual(actual, expected)
        
        #Test sort with pending updates
        tll = Structs.LockableList(values=None)
        tll.extend([5, 3, 4])
        tll.lock(force_update=False)
        tll.extend([0, 1, 2])
        tll.sort()
        actual = tll[:]
        expected = [3, 4, 5]
        self.assertListEqual(actual, expected)
            #Then unlock and test again
        tll.lock(force_update=False)
        tll.sort()
        actual = tll[:]
        expected = [0, 1, 2, 3, 4, 5]
        self.assertListEqual(actual, expected)
    
    def test_properties(self):
        #Check HasPendingUpdates, IsLocked, ChangedSinceLastCall
        tll = Structs.LockableList(values=None)
        
        tll.lock(set_lock=True, force_update=False)
        self.assertFalse(tll.HasPendingUpdates)
        self.assertTrue(tll.IsLocked)
        self.assertFalse(tll.ChangedSinceLastCall)
        
        tll.lock(set_lock=False, force_update=False)
        tll.extend([5, 3, 4])
            #Extending while unlocked shouldn't queue updates
        self.assertFalse(tll.HasPendingUpdates)
        self.assertFalse(tll.IsLocked)
        self.assertTrue(tll.ChangedSinceLastCall)
        tll.clear_change_flag()
        
        tll.lock(set_lock=True, force_update=False)
        tll.extend([0, 1, 2])
            #Now they should be queued
        self.assertTrue(tll.HasPendingUpdates)
        self.assertTrue(tll.IsLocked)
        self.assertTrue(tll.ChangedSinceLastCall)
    
    def test_clear(self):
        #Test normal clear, no lcoks
        tll = Structs.LockableList(values=None)
        tll.extend([3, 4, 5])
        tll.clear()
        self.assertFalse(tll)
        self.assertFalse(tll._to_add)
        self.assertFalse(tll._to_remove)
        
        #Test with lock and pending updates
        tll = Structs.LockableList(values=None)
        tll.extend([3, 4, 5])
        tll.lock()
        tll.extend([100, 200])
        tll.clear()
        self.assertFalse(tll)
        self.assertFalse(tll._to_add)
        self.assertFalse(tll._to_remove)
        

def suite():
    test_suite = unittest.TestSuite()
    suite1 = unittest.makeSuite(EnumTest)
    suite2 = unittest.makeSuite(TypeCheckedListTest)
    suite3 = unittest.makeSuite(DoubleBufferTest)
    suite4 = unittest.makeSuite(LockableListTest)
    test_suite.addTests([suite1, suite2, suite3, suite4])
    return test_suite
    
def load_tests():
    return suite()