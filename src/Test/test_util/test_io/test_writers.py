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
        Util.IO.remove_file(self.filename)
    
    def tearDown(self):
        unittest.TestCase.tearDown(self) 
        Util.IO.remove_file(self.filename)
    
    def test_custom_tid(self):
        #Test that custom starts/stops process in the order
            #They are passed, not numeric order
        log = Writers.Logger(self.filename)
        #Test order: 0( 1( 2( )1 3( )0 )3 )2
        tids = ['jello', 'pudding', 1, -10]
        log.start(tids[0])
        time.sleep(0.35)
        log.start(tids[1])
        time.sleep(0.35)
        log.start(tids[2])
        time.sleep(0.35)
        log.stop(tids[1])
        time.sleep(0.35)
        log.start(tids[3])
        time.sleep(0.35)
        log.stop(tids[0])
        time.sleep(0.35)
        log.stop(tids[3])
        time.sleep(0.35)
        log.stop(tids[2])
        
        #Assert start times are in order
        start = lambda i: log._time_start[tids[i]]
        self.assertTrue(start(0) < start(1))
        self.assertTrue(start(1) < start(2))
        self.assertTrue(start(2) < start(3))
        
        #Assert end times are in order
        end = lambda i: log._time_end[tids[i]]
        self.assertTrue(end(1) < end(0))
        self.assertTrue(end(0) < end(3))
        self.assertTrue(end(3) < end(2))
        
    
    def test_auto_tid(self):
        log = Writers.Logger(self.filename)
        #Test that chronological ordering is kept for
            #tid start/stops.
        tid_start = []
        tid_end = []
        for i in xrange(4):
            tid_start.append(log.start())
            time.sleep(0.35)
        for i in xrange(4):
            tid_end.append(log.stop())
            time.sleep(0.35)
        
        #Assert start times are in order
        start = lambda i: log._time_start[tid_start[i]]
        self.assertTrue(start(0) < start(1))
        self.assertTrue(start(1) < start(2))
        self.assertTrue(start(2) < start(3))
        
        #Assert end times are in order
        end = lambda i: log._time_end[tid_end[i]]
        self.assertTrue(end(0) < end(1))
        self.assertTrue(end(1) < end(2))
        self.assertTrue(end(2) < end(3))
        
        #Assert lists are reversed
        self.assertListEqual(tid_start, list(reversed(tid_end)))
    
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