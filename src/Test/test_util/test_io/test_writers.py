import unittest
import time

import Util.IO.Writers as Writers
import Util.IO

class BufferedWriteTest(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        
        #Where we'll write to
        self.filename = 'temp_writer_test_file.txt'
    
    def tearDown(self):
        unittest.TestCase.tearDown(self) 
        Util.IO.remove_file(self.filename)
    
    def test_buffer_sizes(self):
        #Test 0 buffer
        
        #Test 10 buffer
        
        pass
    
    def test

def suite():
    suite1 = unittest.makeSuite(BufferedWriteTest)
    return unittest.TestSuite(suite1)
    
def load_tests():
    return suite()