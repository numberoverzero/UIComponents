import unittest
import Util.IO.Readers as Readers

class FullBufferedReadTest(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        
        #Set up a file to read
        self.nlines = 120000
        self.single_line = "This is line {}.\n"
        self.filename = 'temp_reader_test_file.txt'
        
        with open(self.filename, 'w', 8 << 10) as f:
            for i in xrange(self.nlines):
                f.write(self.single_line.format(i))
    
    def tearDown(self):
        unittest.TestCase.tearDown(self) 
        import os
        try:
            os.remove(self.filename)
        except WindowsError:
            pass
         
    def test_errors(self):
        #None filename
        with self.assertRaises(IOError):
            fbr = Readers.FullBufferedRead(None)
        
        #Bad filename
        with self.assertRaises(IOError):
            fbr = Readers.FullBufferedRead(":-_!@%..>..")
        
    def test_clear(self):
        #Test that we can't len, getitem
        fbr = Readers.FullBufferedRead(self.filename)
        fbr.clear()
        
        expected = 0
        actual = len(fbr)
        self.assertEqual(actual, expected)
        
        with self.assertRaises(IOError):
            fbr[0]
    
    def test_getitem(self):
        #Test every line is correctly read
        fbr = Readers.FullBufferedRead(self.filename)
        
        for i in xrange(self.nlines):
            expected = self.single_line.format(i)
            actual = fbr[i]
            self.assertEqual(actual, expected)
    
def suite():
    suite1 = unittest.makeSuite(FullBufferedReadTest)
    return unittest.TestSuite(suite1)
    
def load_tests():
    return suite()