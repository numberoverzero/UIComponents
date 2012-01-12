import unittest
import Util.IO as IO

class FmtTimeTest(unittest.TestCase):
    def test_fmt_date(self):
        #IO.file_fmt_date(date_)
        self.skipTest("Not Yet Implemented")
    
    def test_fmt_time(self):
        #IO.file_fmt_time(time_)
        self.skipTest("Not Yet Implemented")
    
    def test_fmt_datetime(self):
        #IO.file_fmt_datetime(datetime_)
        self.skipTest("Not Yet Implemented")

def suite():
    suite1 = unittest.makeSuite(FmtTimeTest)
    return unittest.TestSuite(suite1)
    
def load_tests():
    return suite()