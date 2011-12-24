import unittest
import Util.Formatting as Formatting

class FormattingTest(unittest.TestCase):

    def test_surrounded_by_parens(self):
        #Test each of the parens types
        parens = ['()','{}','[]']
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
        
    def test_str2tuple(self):
        #Test int parsing with parens
        s = "(1,2,3,4,5)"
        expected = (1,2,3,4,5)
        actual = Formatting.str2tuple(s, int, True)
        self.assertEqual(expected, actual)
        
        #Test int parsing without parens
        s = "1,2,3,4,5"
        expected = (1,2,3,4,5)
        actual = Formatting.str2tuple(s, int, False)
        self.assertEqual(expected, actual)
        
        #Test passing string w/parens when specifying it doesn't have them
        s = "[1,2,3]"
        with self.assertRaises(ValueError):
            actual = Formatting.str2tuple(s, int, False)
            
        #Test passing string w/o parens when specifying it has them
        s = "(1,2,3}"
        with self.assertRaises(ValueError):
            actual = Formatting.str2tuple(s, int, True)
        
        #Test str parsing with parens
        s = "{1,2,3,4,5}"
        expected = ('1','2','3','4','5')
        actual = Formatting.str2tuple(s, str, True)
        self.assertEqual(expected, actual)
        
        #Test str parsing without parens
        s = "1,2,3,4,5"
        expected = ('1','2','3','4','5')
        actual = Formatting.str2tuple(s, str, False)
        self.assertEqual(expected, actual)

def suite():
    suite1 = unittest.makeSuite(FormattingTest)
    return unittest.TestSuite(suite1)
    
def load_tests():
    return suite()