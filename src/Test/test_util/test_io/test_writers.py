import unittest
import time

import Util.IO.Writers as Writers

class BufferedWriteTest(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        
        #Where we'll write to
        self.filename = 'temp_writer_test_file.txt'
            
    def tearDown(self):
        unittest.TestCase.tearDown(self) 
        import os
        try:
            os.remove(self.filename)
        except WindowsError:
            pass

def suite():
    suite1 = unittest.makeSuite(BufferedWriteTest)
    return unittest.TestSuite(suite1)
    
def load_tests():
    return suite()