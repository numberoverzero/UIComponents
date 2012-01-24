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
    def setUp(self):
        unittest.TestCase.setUp(self)
        def mk_and_append(size, string):
            sb = Formatting.StringBuilder(size=size)
            for c in string:
                sb += c
            return sb
        self.mk_and_append = mk_and_append
    def test_size(self):
        #test negative size - shouldn't ever build
        sb = self.mk_and_append(-3, "Hello")
        expected = 5
        actual = len(sb.data)
        self.assertEqual(actual, expected)
        
        
        #test 0 size - shouldn't ever build
        sb = self.mk_and_append(0, "Hello")
        expected = 5
        actual = len(sb.data)
        self.assertEqual(actual, expected)
        
        #test 1 size - should build every call
        sb = self.mk_and_append(1, "Hello")
        expected = 1
        actual = len(sb.data)
        self.assertEqual(actual, expected)
        
        #test pos size - should build every n
        sb = self.mk_and_append(2, "Hello")
        expected = 1
        actual = len(sb.data)
        self.assertEqual(actual, expected)
    
    def test_iops(self):
        #Test +=
        sb = self.mk_and_append(5, "Yup")
        sb += ", Bro"
        self.assertTrue(isinstance(sb, Formatting.StringBuilder))
        
        #Test *=
        sb = self.mk_and_append(5, "Yup")
        sb *= 3
        self.assertTrue(isinstance(sb, Formatting.StringBuilder))
        
    def test_ops(self):
        #Test +
        sb = self.mk_and_append(10, "")
        a_string = "Hello"
        
        concat1 = sb + a_string
        concat2 = a_string + sb
        
        self.assertTrue(isinstance(concat1, basestring))
        self.assertTrue(isinstance(concat2, basestring))
        
        #Test <, <=, >, >=, ==, !=
        sb = self.mk_and_append(15, "dog")
        
        self.assertTrue(sb < "elephant")
        
        self.assertTrue(sb <= "elephant")
        self.assertTrue(sb <= "dog")
        
        self.assertTrue(sb == "dog")
        self.assertTrue(sb != "Dog")
        
        self.assertTrue(sb >= "dog")
        self.assertTrue(sb >= "cat")
        
        self.assertTrue(sb > "cat")
    
    def test_overloaded_fns(self):
        #Test in
        sb = self.mk_and_append(10, "burger")
        self.assertTrue("b" in sb)
        self.assertTrue("r" in sb)
        self.assertTrue("g" in sb)
        self.assertFalse("i" in sb)
        
        #Test slicing
        sb = self.mk_and_append(10, "burger")
        s = "burger"
        self.assertEqual(sb[:], s[:])
        self.assertEqual(sb[1:-1], s[1:-1])
        self.assertEqual(sb[1:4], s[1:4])
        self.assertEqual(sb[3:], s[3:])
        self.assertEqual(sb[:-3], s[:-3])
        
        #test len with large append
        sb = self.mk_and_append(10, "burger")
        s = "burger"
        self.assertEqual(len(sb), len(s))
        
        sb += " king makes you fat"
        s += " king makes you fat"
        self.assertEqual(len(sb), len(s))
        
        #test len with multiple small appends
        sb = self.mk_and_append(10, "burger")
        s = "burger"
        self.assertEqual(len(sb), len(s))
        
        for c in " king makes you fat":
            sb += c
        s += " king makes you fat"
        self.assertEqual(len(sb), len(s))
        
def suite():
    test_suite = unittest.TestSuite()
    suite1 = unittest.makeSuite(FormattingTest)
    suite2 = unittest.makeSuite(FormattingTest)
    test_suite.addTests([suite1, suite2])
    return test_suite
    
def load_tests():
    return suite()