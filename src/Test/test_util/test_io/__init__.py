import unittest
import Util.IO as IO

class FmtTimeTest(unittest.TestCase):
    def test_fmt_date(self):
        now = IO.time.localtime()
        actual = IO.file_fmt_date(now)
        expected = IO.time.strftime(IO.FMT_DATE, now)
        self.assertEqual(expected, actual)
    
    def test_fmt_time(self):
        now = IO.time.localtime()
        actual = IO.file_fmt_time(now)
        expected = IO.time.strftime(IO.FMT_TIME, now)
        self.assertEqual(expected, actual)
    
    def test_fmt_datetime(self):
        now = IO.time.localtime()
        actual = IO.file_fmt_datetime(now)
        expected = IO.time.strftime(IO.FMT_DATETIME, now)
        self.assertEqual(expected, actual)

def suite():
    suite1 = unittest.makeSuite(FmtTimeTest)
    return unittest.TestSuite(suite1)
    
def load_tests():
    return suite()