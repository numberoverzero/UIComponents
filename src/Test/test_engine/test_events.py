import unittest
import Engine
import Engine.Events as Events

class EventArgsTest(unittest.TestCase):
    def test_ALL_the_args(self):
        #Test custom_id
        Event1 = Events.EventArgs(custom_id = -100)
        Event2 = Events.EventArgs(custom_id = -100)
        self.assertEqual(Event1.ID, Event2.ID)
        
        Event1 = Events.EventArgs(custom_id = -100)
        Event2 = Events.EventArgs(custom_id = 2500)
        self.assertNotEqual(Event1.ID, Event2.ID)
        
        #Test global_manager
        Event1 = Events.EventArgs()
        Event2 = Events.EventArgs()
        self.assertNotEqual(Event1.ID, Event2.ID)
        
        Engine.GLOBAL_ID_MANAGER.reset()
        
        #Test that resetting a global_manager is bad
        #===================================
        Event1 = Events.EventArgs()
        
        #THIS IS OBVIOUSLY NOT GOOD
        Engine.GLOBAL_ID_MANAGER.reset()
        
        Event2 = Events.EventArgs()
        self.assertEqual(Event1.ID, Event2.ID)
        #===================================
        
        
        #Test custom_manager
        id_manager1 = Engine.id_manager()
        id_manager2 = Engine.id_manager()
        Event1 = Events.EventArgs(id_manager = id_manager1)
        Event2 = Events.EventArgs(id_manager = id_manager2)
        
        #In the future, perhaps different managers will append different prefixes,
            #so as to make these unequal.
        self.assertEqual(Event1.ID, Event2.ID)
        
class EventHandlerTest(unittest.TestCase):
    def test_constructor(self):
        pass
    
    def test_add_handler(self):
        pass
    
    def test_remove_handler(self):
        pass
    
    def test_invoke_empty(self):
        pass
    
    def test_invoke_withargs(self):
        pass
    
    def test_invoke_on_none(self):
        pass
    
    def test_del(self):
        pass
    
def suite():
    test_suite = unittest.TestSuite()
    suite1 = unittest.makeSuite(EventArgsTest)
    suite2 = unittest.makeSuite(EventHandlerTest)
    test_suite.addTests([suite1, suite2])
    return test_suite
    
def load_tests():
    return suite()