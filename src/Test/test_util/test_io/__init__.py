import unittest
import Util.IO as IO

class IOTest(unittest.TestCase):
    def test_bufcount(self):
        nline = 12011
        data = "\n"*nline
        filename = "test_bufcount.txt"
        with open(filename, 'w') as f:
            f.write(data)
        
        expected = nline
        actual = IO.bufcount(filename)
        self.assertEqual(actual, expected)
        import os
        os.remove(filename)
    
    def test_ensdir(self):
        #Test a bad folder name
        path = "!@#$%^&*():;[]{}"
        with self.assertRaises(WindowsError):
            IO.ensdir(path)
        
        import os, os.path
        #Make sure the folder isn't there
        path = "/test_ensdir_folder"
        if os.path.isdir(path): os.rmdir(path)
        
        self.assertFalse(os.path.isdir(path))
        IO.ensdir(path)
        self.assertTrue(os.path.isdir(path))
        os.rmdir(path)
        
    def test_ensfile(self):
        #Test a bad filename
        filename = "!@#$%^&*():;[]{}.txt"
        with self.assertRaises(WindowsError):
            IO.ensfile(filename)
        
        import os, os.path
        #Make sure the folder isn't there
        path = "/test_ensdir_folder"
        filename = "/test_ensdir_folder/test_ensfile.txt"
        if os.path.isfile(filename): os.remove(filename)
        if os.path.isdir(path): os.rmdir(path)
        
        self.assertFalse(os.path.isfile(filename))
        IO.ensfile(filename)
        self.assertTrue(os.path.isfile(filename))
        os.remove(filename)
        os.rmdir(path)

def suite():
    suite1 = unittest.makeSuite(IOTest)
    return unittest.TestSuite(suite1)
    
def load_tests():
    return suite()