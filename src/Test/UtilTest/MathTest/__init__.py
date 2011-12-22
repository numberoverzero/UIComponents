import unittest
import Util.Math as Math

class MathTester(unittest.TestCase):
    
    def assertAlmostEqualSequence(self, first, second, 
                               places = None, msg = None, delta = None):
        n = min(len(first),len(second))
        for i in xrange(n):
            self.assertAlmostEqual(first[i], second[i], places, msg, delta)
    
    def test_iwrap(self):
        #Test negative wrapping
        x = -1
        M = 10
        expected = 9
        actual = Math.iwrap(x,M)
        self.assertEqual(expected, actual)
        
        #Test Positive wrapping
        x = 12
        M = 10
        expected = 2
        actual = Math.iwrap(x,M)
        self.assertEqual(expected, actual)
        
        #Test in-range wrapping
        x = 3
        M = 10
        expected = 3
        actual = Math.iwrap(x,M)
        self.assertEqual(expected, actual)
    
    def test_fwrap(self):
        #Test negative wrapping (all floats) eps = 1E-3
        x = -2.0
        m = 4.0
        M = 8.0
        expected = 6.0
        actual = Math.fwrap(x,m,M)
        self.assertAlmostEqual(expected, actual, 3)
        
        #Test pos val, below min wrapping
        x = 3.5
        m = 5.0
        M = 8.0
        expected = 6.5
        actual = Math.fwrap(x,m,M)
        self.assertAlmostEqual(expected, actual, 3)
        
        #Test neg val above max wrapping
        x = -8.5
        m = -4.0
        M = -7.0
        expected = -5.5
        actual = Math.fwrap(x,m,M)
        self.assertAlmostEqual(expected, actual, 3)
        
        #Test pos val above max wrapping (all floats) eps = 1E-3
        x = 8.5
        m = 4.0
        M = 8.0
        expected = 4.5
        actual = Math.fwrap(x,m,M)
        self.assertAlmostEqual(expected, actual, 3)
        
        #Test in-range wrapping (all floats) eps = 1E-3
        x = 3.75
        m = 2.15
        M = 8.35
        expected = 3.75
        actual = Math.fwrap(x,m,M)
        self.assertAlmostEqual(expected, actual, 3)
        
    def test_clamp(self):
        #Test < min
        v = 1.0
        vmin = 3.0
        vmax = 5.0
        expected = 3.0
        actual = Math.clamp(v, vmin, vmax)
        self.assertAlmostEqual(expected, actual, 3)
        
        #Test > max
        v = 8.0
        vmin = 3.0
        vmax = 5.0
        expected = 5.0
        actual = Math.clamp(v, vmin, vmax)
        self.assertAlmostEqual(expected, actual, 3)
        
        #Test in range
        v = 4.0
        vmin = 3.0
        vmax = 5.0
        expected = 4.0
        actual = Math.clamp(v, vmin, vmax)
        self.assertAlmostEqual(expected, actual, 3)
    
    def test_rotate(self):
        ox = oy = py = 0
        px = 1
        theta = Math.PI / 2
        expected = (0, 1)
        actual = Math.rotate(ox, oy, px, py, theta)
        self.assertAlmostEqualSequence(expected, actual, 5)
    
    def test_unitV(self):
        #Test quad 1
        v = (1, 1)
        expected = (2 ** -0.5, 2 ** -0.5)
        actual = Math.unitV(*v)
        self.assertAlmostEqualSequence(expected, actual, 5)
        
        #Test quad 2
        v = (-1, 1)
        expected = (-(2 ** -0.5), 2 ** -0.5)
        actual = Math.unitV(*v)
        self.assertAlmostEqualSequence(expected, actual, 5)
        
        #Test vertical
        v = (0, 5)
        expected = (0, 1)
        actual = Math.unitV(*v)
        self.assertAlmostEqualSequence(expected, actual, 5)
        
        #Test horizontal
        v = (-4, 0)
        expected = (-1, 0)
        actual = Math.unitV(*v)
        self.assertAlmostEqualSequence(expected, actual, 5)
    
    def test_limV(self):
        pass
    
    def test_angleFromVector(self):
        pass
    
    def test_distance(self):
        pass
    
    def test_isZero(self):
        pass
    
    def test_normalize(self):
        pass
    
    def test_Math_trig_tables(self):
        tt = Math.trig_tables
        
        #Check at 2x resolution
        has_errors, errors = tt.check_all(2)
        msg = "Errors on indices: {0}".format(str(errors))
        self.assertFalse(has_errors, msg)