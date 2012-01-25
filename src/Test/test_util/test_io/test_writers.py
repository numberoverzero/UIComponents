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
    
    def test_write_and_writeln(self):
        #Test 0 buffer
        
        #Test 10 buffer
        
        pass
    
    def test_close_and_force_write(self):
        #Test 0 buffer
        
        #Test 10 buffer
        
        pass

class LoggerTest(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        
        #Where we'll write to
        self.filename = 'temp_logger_test_file.txt'
    
    def tearDown(self):
        unittest.TestCase.tearDown(self) 
        Util.IO.remove_file(self.filename)
    
    def test_custom_tid(self):
        #Test that custom starts/stops process in the order
            #They are passed, not numeric order
        pass
    
    def test_auto_tid(self):
        #Test that chronological ordering is kept for
            #tid start/stops.
        pass
    
    def test_log_msg(self):
        #Test log msg without tid
        
        #Test log msg with tid
        
        pass
    
    def test_log_elapsed(self):
        #Test log elapsed with tid
        
        #Test log elapsed without tid
        
        pass

def suite():
    test_suite = unittest.TestSuite()
    suite1 = unittest.makeSuite(BufferedWriteTest)
    suite2 = unittest.makeSuite(LoggerTest)
    test_suite.addTests([suite1, suite2])
    return test_suite
    
def load_tests():
    return suite()