import unittest
import Util.Math as Math

class MathTest(unittest.TestCase):
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
        #Check in-range values
        v = (-4, 0, 4)
        expected = (-4, 0)
        actual = Math.limV(*v)
        self.assertAlmostEqualSequence(expected, actual, 5)
        
        #Check out-of range positives, and vertical vectors
        v = (10, 0, 3.5)
        expected = (3.5, 0)
        actual = Math.limV(*v)
        self.assertAlmostEqualSequence(expected, actual, 5)
        
        #Check out-of-range negatives and multi-direction
        v = (-4, -4, 1)
        expected = (-(2 ** -0.5), -(2 ** -0.5))
        actual = Math.limV(*v)
        self.assertAlmostEqualSequence(expected, actual, 5)
        
        #Check negative mags raise Error
        v = (-4, 0, -3)
        expected = (-4, 0)
        with self.assertRaises(ArithmeticError):
            actual = Math.limV(*v)
    
    def test_angleFromVector(self):
        #We know that math.atan works as expected
        pass
    
    def test_distance(self):
        #Test that zeros work
        p1 = [1,1,1]
        p2 = [0,0,0]
        expected = 3 ** 0.5
        actual = Math.distance(p1, p2)
        self.assertAlmostEqual(expected, actual, 5)
        
        #Test that unequal size vectors fail
        p1 = [1,1,1]
        p2 = [0,0]
        expected = 2 ** 0.5
        with self.assertRaises(IndexError):
            actual = Math.distance(p1, p2)
        
        #Test positive/negative mixing
        p1 = [0,5.5]
        p2 = [0,-7.5]
        expected = 13.0
        actual = Math.distance(p1, p2)
        self.assertAlmostEqual(expected, actual, 5)
        
        #Test orthogonal vectors (not that this should matter tbh)
        p1 = [0,1]
        p2 = [1,0]
        expected = 2 ** 0.5
        actual = Math.distance(p1, p2)
        self.assertAlmostEqual(expected, actual, 5)
        
    def test_isZero(self):
        #Test default precision
        self.assertTrue(Math.isZero(0.000000009))
        
        #Test fail default precision
        self.assertFalse(Math.isZero(0.000000011))
        
        #Test low-precision
        self.assertTrue(Math.isZero(0.001, 2))
        self.assertTrue(Math.isZero(0.01, 1))
        
        #Test negatives
        self.assertTrue(Math.isZero(-1.5E-9))
        
        #Test positives
        self.assertTrue(Math.isZero(-1.5E-9))
        
    def test_normalize(self):
        #Test on single value
        actual = [4.5]
        expected = [1.0]
        Math.normalize(actual)
        self.assertAlmostEqualSequence(expected, actual, 5)
        
        #Test on roughly (isZero) equal values
        actual = [4.5, 4.50000000001, 4.4999999999999]
        expected = [1.0] * len(actual)
        Math.normalize(actual)
        self.assertAlmostEqualSequence(expected, actual, 5)
        
        #Test on negatives
        actual = [-4.0, -4.0]
        expected = [1.0] * len(actual)
        Math.normalize(actual)
        self.assertAlmostEqualSequence(expected, actual, 5)
        
        #Test on positives
        actual = [2.0, 1.5, 1.0]
        expected = [1.0, 0.5, 0.0]
        Math.normalize(actual)
        self.assertAlmostEqualSequence(expected, actual, 5)
    
    def test_Math_trig_tables(self):
        tt = Math.trig_tables
        
        #Check at 2x resolution
        has_errors, errors = tt.check_all(2)
        msg = "Errors on indices: {0}".format(str(errors))
        self.assertFalse(has_errors, msg)
        
def suite():
    suite1 = unittest.makeSuite(MathTest)
    return unittest.TestSuite(suite1)
    
def load_tests():
    return suite()