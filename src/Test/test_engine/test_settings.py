import unittest
import Engine.Settings as Settings

class SettingTest(unittest.TestCase):
    def test_current_index(self):
        options = ["Option0", "Option1", "Option2"]
        setting = Settings.Setting(name="MySetting",
                                   description="A test setting",
                                   default=0, selection=1,
                                   options=options)
        
        #Assert we assigned selection correctly
        expected = 1
        actual = setting.current_index
        self.assertEqual(actual, expected)
        
        #Change index to one in range
        setting.current_index += 1
        
        expected = 2
        actual = setting.current_index
        self.assertEqual(actual, expected)
        
        #Change index to 3, which should wrap to 0
        setting.current_index += 1
        
        expected = 0
        actual = setting.current_index
        self.assertEqual(actual, expected)
    
    def test_default_index(self):
        options = ["Option0", "Option1", "Option2"]
        setting = Settings.Setting(name="MySetting",
                                   description="A test setting",
                                   default=1, selection=0,
                                   options=options)
        
        #Assert we assigned selection correctly
        expected = 1
        actual = setting.default_index
        self.assertEqual(actual, expected)
        
        #Change index to one in range
        setting.default_index += 1
        
        expected = 2
        actual = setting.default_index
        self.assertEqual(actual, expected)
        
        #Change index to 3, which should wrap to 0
        setting.default_index += 1
        
        expected = 0
        actual = setting.default_index
        self.assertEqual(actual, expected)
    
    def test_current_option(self):
        options = ["Option0", "Option1", "Option2"]
        setting = Settings.Setting(name="MySetting",
                                   description="A test setting",
                                   default=1, selection=0,
                                   options=options)
        
        #Assert we assigned selection correctly
        expected = "Option0"
        actual = setting.current_option
        self.assertEqual(actual, expected)
        
        #Change current to one in options
        setting.current_option = "Option2"
        
        expected = "Option2"
        actual = setting.current_option
        self.assertEqual(actual, expected)
        
        #Change item to one not in options
        with self.assertRaises(KeyError):
            setting.current_option = "Not Possible Option"
    
    def test_next_option(self):
        options = ["Option0", "Option1", "Option2"]
        setting = Settings.Setting(name="MySetting",
                                   description="A test setting",
                                   default=1, selection=0,
                                   options=options)
        
        #Assert we assigned selection correctly
        expected = "Option1"
        actual = setting.next_option
        self.assertEqual(actual, expected)
        
        #Check next
        setting.current_index += 1
        
        expected = "Option2"
        actual = setting.next_option
        self.assertEqual(actual, expected)
        
        #Check next- a wrapped next
        setting.current_index += 1
        
        expected = "Option0"
        actual = setting.next_option
        self.assertEqual(actual, expected)
    
    def test_previous_option(self):
        options = ["Option0", "Option1", "Option2"]
        setting = Settings.Setting(name="MySetting",
                                   description="A test setting",
                                   default=1, selection=0,
                                   options=options)
        
        #Assert we assigned selection correctly
        expected = "Option2"
        actual = setting.previous_option
        self.assertEqual(actual, expected)
        
        #Check previous
        setting.current_index += 1
        
        expected = "Option0"
        actual = setting.previous_option
        self.assertEqual(actual, expected)
        
        #Check previous
        setting.current_index += 1
        
        expected = "Option1"
        actual = setting.previous_option
        self.assertEqual(actual, expected)
    
    def test_add_option(self):
        options = []
        setting = Settings.Setting(name="MySetting",
                                   description="A test setting",
                                   default=1, selection=0,
                                   options=options)
        
        #Make sure we start empty
        self.assertListEqual(options, setting.options)
        
        #Add an option
        options.append("Yellow")
        setting.add_option("Yellow")
        
        #Check it added
        self.assertListEqual(options, setting.options)
        
        #Right now multiple of the same option can be added- check it
        options.append("Yellow")
        setting.add_option("Yellow")
        
        #Check it added
        self.assertListEqual(options, setting.options)
    
    def test_remove_option(self):
        options = ["Option0", "Option1", "Option2"]
        setting = Settings.Setting(name="MySetting",
                                   description="A test setting",
                                   default=1, selection=0,
                                   options=options)
        
        #Make sure we start with all options
        self.assertListEqual(options, setting.options)
        
        #Remove an option
        options.remove("Option1")
        setting.remove_option("Option1")
        
        #Check it removed
        self.assertListEqual(options, setting.options)
        
        #Remove all items, check we're empty, check current_index
        options.remove("Option2")
        setting.remove_option("Option2")
        options.remove("Option0")
        setting.remove_option("Option0")
        
        expected = -1
        actual = setting.current_index
        self.assertEqual(actual, expected)
    
    def test_load_using_config_parser(self):
        self.skipTest("Not Yet Implemented")
    
    def test_save_using_config_parser(self):
        self.skipTest("Not Yet Implemented")
    
class SettingsTest(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        options = ["Option0", "Option1", "Option2"]
        self.my_setting = Settings.Setting(name="MySetting",
                                   description="A test setting",
                                   default=0, selection=1,
                                   options=options)
        color_options = ["Yellow", "Red", "Blue"]
        self.color_setting = Settings.Setting(name="ColorSetting",
                                   description="Pick a color",
                                   default=0, selection=0,
                                   options=color_options)
        
        #New settings object
        self.settings = Settings.Settings()
        #Add in settings using __setitem__
        self.settings["MySetting"] = self.my_setting
        self.settings["ColorSetting"] = self.color_setting
        
    def test_load(self):
        self.skipTest("Not Yet Implemented")
    
    def test_save(self):
        self.skipTest("Not Yet Implemented")
        
    def test_add_setting(self):
        
        original_len = len(self.settings)
        
        new_setting = Settings.Setting()
        self.settings.add_setting("Junk_Setting", new_setting)
        
        new_len = len(self.settings)
        
        expected = 1
        actual = new_len - original_len
        self.assertEqual(expected, actual)
        
        sb_new_setting = self.settings["Junk_Setting"]
        self.assertEqual(new_setting, sb_new_setting)
    
    def test_remove_setting(self):
        
        original_len = len(self.settings)
        
        self.settings.remove_setting("ColorSetting")
        
        with self.assertRaises(KeyError):
            self.settings["ColorSetting"]
        
        new_len = len(self.settings)
        
        expected = -1
        actual = new_len - original_len
        self.assertEqual(expected, actual)
    
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