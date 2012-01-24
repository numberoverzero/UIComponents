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
        path = "!@#$%^&*():;[]{}+-`~\"/|"
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
        with self.assertRaises(IOError):
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
    
    def test_remove_file(self):
        #Test file that doesn't exist
        result = IO.remove_file("sadksal21r45ewq90&&&&%%!@####:::")
        self.assertFalse(result)
        
        #Test file that does exist
        IO.ensfile("test_remove_file.exe")
        result = IO.remove_file("test_remove_file.exe")
        self.assertTrue(result)
        
        #Test file that exists, but can't be removed.
        IO.ensfile("test_remove_file.txt")
        with open("test_remove_file.txt") as f:
            result = IO.remove_file("test_remove_file.txt")
            self.assertFalse(result)
        result = IO.remove_file("test_remove_file.txt")
        self.assertTrue(result)
def suite():
    suite1 = unittest.makeSuite(IOTest)
    return unittest.TestSuite(suite1)
    
def load_tests():
    return suite()