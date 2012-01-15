import unittest
import Engine.ID as ID

class IDTest(unittest.TestCase):
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
        self.id_fmt_int = "None:Test.test_engine.test_id.o_int:{}"
        self.id_fmt_str = "None:Test.test_engine.test_id.o_str:{}"
        
    def test_id_manager_instanced_version(self):
        #Make a new manager
        id_manager = ID.id_manager()
        
        #Make some int objects
        int_objs = []
        for i in range(10):
            int_objs.append(self.mk_obj(id_manager, self.o_int))
        
        #Make a str object
        str_obj = self.mk_obj(id_manager, self.o_str)
        
        for i in range(10):
            expected = self.id_fmt_int.format(i)
            actual = int_objs[i]._id
            self.assertEqual(actual, expected)
        
        actual = str_obj._id
        expected = self.id_fmt_str.format(0)
        self.assertEqual(actual, expected)
        
        #Add another int
        int_objs.append(self.mk_obj(id_manager, self.o_int))
        actual = int_objs[-1]._id
        expected = self.id_fmt_int.format(10)
        self.assertEqual(actual, expected)
        
    def test_id_manager_global_version(self):
        #Do a reset
        id_manager = ID.GLOBAL_ID_MANAGER
        id_manager.reset()
        
        #Global id strings
        g_int_fmt = "GLOBAL:Test.test_engine.test_id.o_int:{}"
        g_str_fmt = "GLOBAL:Test.test_engine.test_id.o_str:{}"
        
        #Make some int objects
        int_objs = []
        for i in range(10):
            int_objs.append(self.mk_obj(id_manager, self.o_int))
        
        #Make a str object
        str_obj = self.mk_obj(id_manager, self.o_str)
        
        for i in range(10):
            expected = g_int_fmt.format(i)
            actual = int_objs[i]._id
            self.assertEqual(actual, expected)
        
        actual = str_obj._id
        expected = g_str_fmt.format(0)
        self.assertEqual(actual, expected)
        
        #Add another int
        int_objs.append(self.mk_obj(id_manager, self.o_int))
        actual = int_objs[-1]._id
        expected = g_int_fmt.format(10)
        self.assertEqual(actual, expected)
        
        #Test a reset and do it one more time
        id_manager.reset()
        
        #Make some int objects
        int_objs = []
        for i in range(10):
            int_objs.append(self.mk_obj(id_manager, self.o_int))
        
        #Make a str object
        str_obj = self.mk_obj(id_manager, self.o_str)
        
        for i in range(10):
            expected = g_int_fmt.format(i)
            actual = int_objs[i]._id
            self.assertEqual(actual, expected)
        
        actual = str_obj._id
        expected = g_str_fmt.format(0)
        self.assertEqual(actual, expected)
        
        #Add another int
        int_objs.append(self.mk_obj(id_manager, self.o_int))
        actual = int_objs[-1]._id
        expected = g_int_fmt.format(10)
        self.assertEqual(actual, expected)
        
        #Clear out the global again
        id_manager.reset()
    
    def test_id(self):
        a = ID.ID(custom_value = -100)
        b = ID.ID(custom_value = -200)
        c = ID.ID(custom_value = -100)
        
        self.assertEqual(a, c)
        self.assertNotEqual(a, b)
        self.assertNotEqual(b, c)
        
        ID.GLOBAL_ID_MANAGER.reset()
        
        d = ID.ID()
        e = ID.ID()
        
        self.assertNotEqual(d, e)
        
        ID.GLOBAL_ID_MANAGER.reset()

def suite():
    suite1 = unittest.makeSuite(IDTest)
    return unittest.TestSuite(suite1)
    
def load_tests():
    return suite()