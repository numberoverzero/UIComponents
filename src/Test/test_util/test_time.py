import unittest
import Util.Time as Time

class FmtTimeTest(unittest.TestCase):
    def test_fmt_date(self):
        now = Time.time.localtime()
        actual = Time.file_fmt_date(now)
        expected = Time.time.strftime(Time.FMT_DATE, now)
        self.assertEqual(expected, actual)
    
    def test_fmt_time(self):
        now = Time.time.localtime()
        actual = Time.file_fmt_time(now)
        expected = Time.time.strftime(Time.FMT_TIME, now)
        self.assertEqual(expected, actual)
    
    def test_fmt_datetime(self):
        now = Time.time.localtime()
        actual = Time.file_fmt_datetime(now)
        expected = Time.time.strftime(Time.FMT_DATETIME, now)
        self.assertEqual(expected, actual)
    
    def test_log_fmt_time(self):
        now = Time.time.localtime()
        actual = Time.log_fmt_time(now)
        expected = Time.time.strftime(Time.FMT_LOG_TIME, now)
        self.assertEqual(expected, actual)
    
    def test_split_time(self):
        hrs = 10
        mins = 11
        sec = 12
        ms = 13
        total = hrs * 3600 + mins * 60 + sec + ms / 1000.0
        expected = [hrs, mins, sec, ms]
        actual = list(Time.split_time(total))
        self.assertListEqual(actual, expected)
        
    def test_combine_time(self):
        hrs = 10
        mins = 11
        sec = 12
        ms = 13
        total = hrs * 3600 + mins * 60 + sec + ms / 1000.0
        expected = total
        actual = Time.combine_time(hrs, mins, sec, ms)
        self.assertAlmostEqual(actual, expected, 5)

def suite():
    suite1 = unittest.makeSuite(FmtTimeTest)
    return unittest.TestSuite(suite1)
    
def load_tests():
    return suite()