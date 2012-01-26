import unittest
import time

import Util.IO.Writers as Writers
import Util.IO

class BufferedWriteTest(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        
        #Where we'll write to
        self.filename = 'temp_writer_test_file.txt'
        Util.IO.remove_file(self.filename)
    
    def tearDown(self):
        unittest.TestCase.tearDown(self) 
        Util.IO.remove_file(self.filename)
    
    def check_file(self, data):
        with open(self.filename) as filename:
            actual = filename.read()
        self.assertEqual(actual, data)
    
    def test_write_and_writeln_no_buff(self):
        #Test 0 buffer
        #This should immediately write to file
        writer = Writers.BufferedWriter(self.filename, buffer_size = 0)
        data = "Hello"
        writer.write(data)
        self.check_file(data)
        
        data_2 = "\nThis is exciting!"
        writer.writeln(data_2)
        data += data_2 + "\n"
        self.check_file(data)
    
    def test_write_and_writeln_10_buff(self):
        #Test 10 buffer
        #Should be empty the first time because we don't hit limit
        #But on second check, we dump all of the buffer,
            #even though it's longer than 10
        writer = Writers.BufferedWriter(self.filename, buffer_size = 10)
        data = "Hello"
        writer.write(data)
        self.check_file("")
        
        data_2 = "\nThis is exciting!"
        writer.writeln(data_2)
        data += data_2 + "\n"
        self.check_file(data)
        
    def test_close_and_force_write_no_buff(self):
        #Test 0 buffer
        writer = Writers.BufferedWriter(self.filename, buffer_size = 0)
        data = "Hello"
        writer.write(data)
        self.check_file(data)
        writer.close()
        self.check_file(data)
        
        writer = Writers.BufferedWriter(self.filename, buffer_size = 0)
        data_2 = "\nThis is exciting!"
        writer.writeln(data_2)
        data += data_2 + "\n"
        self.check_file(data)
        writer.close()
        self.check_file(data)
        
    def test_close_and_force_write_10_buff(self):
        #Test 10 buffer
        writer = Writers.BufferedWriter(self.filename, buffer_size = 10)
        data = "Hello"
        writer.write(data)
        self.check_file("")
        #This close should trigger a write that we didn't have before
        writer.close()
        self.check_file(data)
        
        writer = Writers.BufferedWriter(self.filename, buffer_size = 10)
        data_2 = "\nThis is exciting!"
        writer.writeln(data_2)
        data += data_2 + "\n"
        self.check_file(data)
        writer.close()
        self.check_file(data)

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