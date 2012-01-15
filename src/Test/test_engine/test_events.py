import functools
import unittest
import Engine
import Engine.Events as Events

class EventArgsTest(unittest.TestCase):
    def test_arg_custom_ids(self):
        Event1 = Events.EventArgs(custom_id= -100)
        Event2 = Events.EventArgs(custom_id= -100)
        self.assertEqual(Event1.eid, Event2.eid)
        
        Event1 = Events.EventArgs(custom_id= -100)
        Event2 = Events.EventArgs(custom_id=2500)
        self.assertNotEqual(Event1.eid, Event2.eid)
    
    def test_arg_global_ids(self):
        Event1 = Events.EventArgs()
        Event2 = Events.EventArgs()
        self.assertNotEqual(Event1.eid, Event2.eid)
    
    def test_arg_global_reset_bad(self):
        #Reset the global so we have a clean slate
        Engine.ID.GLOBAL_ID_MANAGER.reset()
        
        Event1 = Events.EventArgs()
        
        #THIS SHOULD BE OBVIOUSLY BAD
        Engine.ID.GLOBAL_ID_MANAGER.reset()
        
        Event2 = Events.EventArgs()
        self.assertEqual(Event1.eid, Event2.eid)
        
class EventHandlerTest(unittest.TestCase):
    def test_constructor(self):
        a = Events.EventHandler()
        b = Events.EventHandler()
        
        self.assertNotEqual(a, b)
        
        #Force equal
        c_id = 1234
        c = Events.EventHandler(custom_id = c_id)        
        c_copy = Events.EventHandler(custom_id=c_id)
        
        self.assertEqual(c, c_copy)
    
    def test_add_handler(self):
        def listener(sender, eventargs):
            pass
        
        a = Events.EventHandler()
        a.add_listener(listener)
        
        expected = [listener]
        actual = a.Listeners
        self.assertListEqual(actual, expected)
        
        #Make sure a second identical add doesn't actually add.
        a.add_listener(listener)
        expected = [listener]
        actual = a.Listeners
        self.assertListEqual(actual, expected)
    
    def test_remove_handler(self):
        def listener(sender, eventargs):
            pass
        
        a = Events.EventHandler()
        
        #Make sure a remove on empty doesn't blow things up
        a.remove_listener(listener)
        expected = []
        actual = a.Listeners
        self.assertListEqual(actual, expected)
        
        #Add a listener to remove
        a.add_listener(listener)
        
        #Make sure we've got it before we try to remove it
        expected = [listener]
        actual = a.Listeners
        self.assertListEqual(actual, expected)
        
        a.remove_listener(listener)
        expected = []
        actual = a.Listeners
        self.assertListEqual(actual, expected)
        
        #Make sure a second remove doesn't mess things up
        a.remove_listener(listener)
        expected = []
        actual = a.Listeners
        self.assertListEqual(actual, expected)
    
    def test_invoke(self):
        def listener(sender, eventargs):
            raise ArithmeticError
        
        a = Events.EventHandler()
        a += listener
        
        with self.assertRaises(ArithmeticError):
            a.invoke()
    
    def test_invoke_with_sender(self):
        class sender_obj(object):
            triggered = False
        def listener(sender, eventargs):
            sender.triggered = True
        
        a = Events.EventHandler()
        a += listener
        
        #Obj to store results in
        a_sender_obj = sender_obj()
        
        self.assertFalse(a_sender_obj.triggered)
        a.invoke(a_sender_obj)
        self.assertTrue(a_sender_obj.triggered)
    
    def test_invoke_with_sender_with_args(self):
        class sender_obj(object):
            triggered = False
        some_event_args = functools.partial(Events.EventArgs)
        def listener(sender, eventargs):
            sender.triggered = True
            self.assertTrue(eventargs.eid.Value == -100)
        
        a = Events.EventHandler()
        a += listener
        
        #Obj to store results in
        a_sender_obj = sender_obj()
        
        #event args to send
        my_event_args = some_event_args(custom_id= -100)
        
        self.assertFalse(a_sender_obj.triggered)
        a.invoke(a_sender_obj, my_event_args)
        self.assertTrue(a_sender_obj.triggered)
    
    def test_invoke_with_args(self):
        some_event_args = functools.partial(Events.EventArgs)
        def listener(sender, eventargs):
            self.assertTrue(sender is None)
            self.assertEqual(eventargs.eid.Value, -100)
        listener_2 = None
        
        a = Events.EventHandler()
        a += [listener, listener_2]
                
        #event args to send
        my_event_args = some_event_args(custom_id= -100)
        
        a.invoke(event_args = my_event_args)
        
        expected = [listener]
        actual = a.Listeners
        self.assertListEqual(actual, expected)
        
def suite():
    test_suite = unittest.TestSuite()
    suite1 = unittest.makeSuite(EventArgsTest)
    suite2 = unittest.makeSuite(EventHandlerTest)
    test_suite.addTests([suite1, suite2])
    return test_suite
    
def load_tests():
    return suite()