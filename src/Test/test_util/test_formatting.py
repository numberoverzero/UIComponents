import unittest
import Util.Formatting as Formatting

class FormattingTest(unittest.TestCase):

    def test_paren_type_func(self):
        #test tuple
        s = "(tuple1, tuple2)"
        self.assertTrue(Formatting.paren_type_func(s) == tuple)
        
        #test list
        s = "[list1, list2]"
        self.assertTrue(Formatting.paren_type_func(s) == list)
        
        #test default
        s = "[mixed1, mixed2)"
        s_pt_fn = Formatting.paren_type_func(s)
        item = 'mixed 1'
        self.assertEqual(item, s_pt_fn(item))
    
    def test_str_to_struct(self):
        #Test int parsing with parens
        s = "(1,2,3,4,5)"
        expected = (1, 2, 3, 4, 5)
        actual = Formatting.str_to_struct(s, int, True)
        self.assertEqual(expected, actual)
        
        #Test int parsing without parens
        s = "1,2,3,4,5"
        expected = (1, 2, 3, 4, 5)
        actual = Formatting.str_to_struct(s, int, False)
        self.assertEqual(expected, actual)
        
        #Test passing string w/parens when specifying it doesn't have them
        s = "[1,2,3]"
        with self.assertRaises(ValueError):
            actual = Formatting.str_to_struct(s, int, False)
            
        #Test passing string w/o parens when specifying it has them
        s = "(1,2,3}"
        with self.assertRaises(ValueError):
            actual = Formatting.str_to_struct(s, int, True)
        
        #Test str parsing with braces
        s = "{1,2,3,4,5}"
        expected = ('1', '2', '3', '4', '5')
        gen_actual = Formatting.str_to_struct(s, str, True)
        actual = tuple(gen_actual)
        actual = Formatting.str_to_struct(s, str, True)
        
        #Test str parsing without parens
        s = "1,2,3,4,5"
        expected = ('1', '2', '3', '4', '5')
        actual = Formatting.str_to_struct(s, str, False)
        self.assertEqual(expected, actual)
    
    def test_struct_to_str(self):
        #Test numbers
        a = [1, 2, 3]
        a_str = Formatting.struct_to_str(a)
        expected = "[1,2,3]"
        self.assertEqual(a_str, expected)
        
        #Test strings
        a = ['1', '2', '3']
        a_str = Formatting.struct_to_str(a)
        expected = "[1,2,3]"
        self.assertEqual(a_str, expected)
        
        #Test mixed
        a = ['1', 2, '3']
        a_str = Formatting.struct_to_str(a)
        expected = "[1,2,3]"
        self.assertEqual(a_str, expected)
        
    def test_surrounded_by_parens(self):
        #Test each of the parens types
        parens = ['()', '{}', '[]']
        msg = "This contains parens.  "
        for paren in parens:
            s = paren[0] + msg + paren[1]
            expected = Formatting.surrounded_by_parens(s)
            self.assertTrue(expected)
        
        #Test non-equal parens
        s = "(This doesn't have parens.}"
        expected = Formatting.surrounded_by_parens(s)
        self.assertFalse(expected)
        
        #Test single paren
        s = "This doesn't have) parens)"
        expected = Formatting.surrounded_by_parens(s)
        self.assertFalse(expected)
        
        #Test no parens
        s = "There are no parens here."
        expected = Formatting.surrounded_by_parens(s)
        self.assertFalse(expected)

class StringBuilderTest(unittest.TestCase):
    pass

def suite():
    test_suite = unittest.TestSuite()
    suite1 = unittest.makeSuite(FormattingTest)
    suite2 = unittest.makeSuite(FormattingTest)
    test_suite.addTests([suite1, suite2])
    return test_suite
    
def load_tests():
    return suite()