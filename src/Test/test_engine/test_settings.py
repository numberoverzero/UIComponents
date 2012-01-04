import unittest
import Engine.Settings as Settings

class SettingTest(unittest.TestCase):
    def test_constructor(self):
        pass
    
    def test_index(self):
        pass
    
    def test_default(self):
        pass
    
    def test_current(self):
        pass
    
    def test_next_option(self):
        pass
    
    def test_previous_option(self):
        pass
    
    def test_add_option(self):
        pass
    
    def test_remove_option(self):
        pass
    
    def test_load_using_config_parser(self):
        pass
    
    def test_save_using_config_parser(self):
        pass
    
class SettingsTest(unittest.TestCase):
    def test_load(self):
        pass
    
    def test_save(self):
        pass
    
    def test_get_item(self):
        pass
    
    def test_add_setting(self):
        pass
    
    def test_remove_setting(self):
        pass
    
    def test_add_option(self):
        pass
    
    def test_remove_option(self):
        pass

def suite():
    test_suite = unittest.TestSuite()
    suite1 = unittest.makeSuite(SettingTest)
    suite2 = unittest.makeSuite(SettingsTest)
    test_suite.addTests([suite1, suite2])
    return test_suite
    
def load_tests():
    return suite()