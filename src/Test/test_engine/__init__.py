import unittest
import Engine

class EngineTest(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        class o_int(object):
            pass
        class o_str(object):
            pass
        class o_other(object):
            pass
        
        self.o_int = o_int
        self.o_str = o_str
        self.o_other = o_other
        
        def mk_obj(id_manager, dtype):
            if dtype == self.o_int:
                obj = self.o_int()
            elif dtype == self.o_str:
                obj = self.o_str()
            else:
                obj = self.o_other()
            obj._id = id_manager.next_id(obj)
            return obj
                    
            
        self.mk_obj = mk_obj
        
    def test_id_manager(self):
        #Make a new manager
        id_manager = Engine.id_manager()
        
        #Make some int objects
        int_objs = []
        for i in range(10):
            int_objs.append(self.mk_obj(id_manager, self.o_int))
        
        #Make a str object
        str_obj = self.mk_obj(id_manager, self.o_str)
        
        for i in range(10):
            expected = i
            actual = int_objs[i]._id
            self.assertEqual(actual, expected)
        
        actual = str_obj._id
        expected = 0
        self.assertEqual(actual, expected)
        
        #Add another int
        int_objs.append(self.mk_obj(id_manager, self.o_int))
        actual = int_objs[-1]._id
        expected = 10
        self.assertEqual(actual, expected)

def suite():
    suite1 = unittest.makeSuite(EngineTest)
    return unittest.TestSuite(suite1)
    
def load_tests():
    return suite()