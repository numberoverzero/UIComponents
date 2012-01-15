import unittest
import ConfigParser
import Engine.Settings as Settings
import Util.Formatting

class SettingTest(unittest.TestCase):
    def test_current_index(self):
        options = ["Option0", "Option1", "Option2"]
        setting = Settings.Setting(name="MySetting",
                                   description="A test setting",
                                   default_index=0, current_index=1,
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
                                   default_index=1, current_index=0,
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
                                   default_index=1, current_index=0,
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
                                   default_index=1, current_index=0,
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
                                   default_index=1, current_index=0,
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
                                   default_index=1, current_index=0,
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
                                   default_index=1, current_index=0,
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
        config = ConfigParser.ConfigParser()
        name = "Color"
        data = {
                         'description': 'Pick a color',
                         'default_option': 'Blue',
                         'current_option': 'Green',
                         'options': "[Red,Blue,Green,Black]",
                         }
        options_lst = Util.Formatting.str_to_struct(data['options'], str)
        
        config.add_section(name)
        for option in data.keys():
            config.set(name, option, data[option])
        
        a_setting = Settings.Setting()
        a_setting.load(config, name)
        
        self.assertEqual(data['description'], a_setting.description)
        self.assertEqual(data['default_option'], a_setting.options[a_setting.default_index])
        self.assertEqual(data['current_option'], a_setting.current_option)
        self.assertEqual(options_lst, a_setting.options)
    
    def test_save_using_config_parser(self):
        config = ConfigParser.ConfigParser()
        
        name = "Color"
        data = {
                         'description': 'Pick a color',
                         'default_option': 'Blue',
                         'current_option': 'Green',
                         'options': "[Red,Blue,Green,Black]",
                         }
        options_lst = Util.Formatting.str_to_struct(data['options'], str)
        
        a_setting = Settings.Setting(name=name, description=data['description'],
                                     default_index=1,
                                     current_index=2,
                                     options=options_lst)
        
        a_setting.save(config, name)
        
        self.assertEqual(data['description'], config.get(name, 'description'))
        self.assertEqual(data['default_option'], config.get(name, 'default_option'))
        self.assertEqual(data['current_option'], config.get(name, 'current_option'))
        config_opts = config.get(name, 'options')
        setting_opts = Util.Formatting.str_to_struct(config_opts, str)
        self.assertEqual(options_lst, setting_opts)
    
class SettingsTest(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        options = ["Option0", "Option1", "Option2"]
        self.my_setting = Settings.Setting(name="MySetting",
                                   description="A test setting",
                                   default_index=0, current_index=1,
                                   options=options)
        color_options = ["Yellow", "Red", "Blue"]
        self.color_setting = Settings.Setting(name="ColorSetting",
                                   description="Pick a color",
                                   default_index=0, current_index=0,
                                   options=color_options)
        
        #New settings object
        self.settings = Settings.Settings()
        #Add in settings using __setitem__
        self.settings["MySetting"] = self.my_setting
        self.settings["ColorSetting"] = self.color_setting
        
    def test_load(self):
        filename = "test_load_settings.ini"
        write_file = open(filename, 'w')
        write_file.write("")
        write_file.close()
        
        def write(line):
            write_file = open(filename, 'a')
            write_file.write(line+"\n")
            write_file.close()
        
        sections = ['Color', 'Resolution', 'Food']
        data_color = {
                         'description': 'Pick a color',
                         'default_option': 'Blue',
                         'current_option': 'Green',
                         'options': "[Red,Blue,Green,Black]",
                         }
        data_res = {
                         'description': 'Screen resolution',
                         'default_option': '600x400',
                         'current_option': '1920x1080',
                         'options': "[600x400,1024x768,1920x1080,1920x1200]",
                         }
        data_food = {
                         'description': 'Favorite food',
                         'default_option': 'Broccoli',
                         'current_option': 'Ice Cream',
                         'options': "[Pizza, Steak, Ice Cream, Broccoli]",
                         }
        datas = [data_color, data_res, data_food]
        
        nopts = len(sections)
        for i in xrange(nopts):
            section = sections[i]
            data = datas[i]
            #Write section header
            write("["+section+"]")
            
            #Write the options
            for option in data.keys():
                write(option+": "+data[option])
            
            #Single space between settings
            write("")
        
        settings = Settings.Settings(filename)
        settings.load()
        
        for i in xrange(nopts):
            setting_name = sections[i]
            setting = settings[setting_name]
            data = datas[i]
            self.assertEqual(data['description'], setting.description)
            self.assertEqual(data['default_option'], setting.default_option)
            self.assertEqual(data['current_option'], setting.current_option)
            opts = Util.Formatting.str_to_struct(data['options'], str)
            self.assertEqual(opts, setting.options)
            
        import os
        try:
            os.remove(filename)
        except WindowsError:
            pass
                
    def test_save(self):
        filename = "test_load_settings.ini"
        
        sections = ['Color', 'Resolution', 'Food']
        data_color = {
                         'description': 'Pick a color',
                         'default_option': 'Blue',
                         'current_option': 'Green',
                         'options': "[Red,Blue,Green,Black]",
                         }
        data_res = {
                         'description': 'Screen resolution',
                         'default_option': '600x400',
                         'current_option': '1920x1080',
                         'options': "[600x400,1024x768,1920x1080,1920x1200]",
                         }
        data_food = {
                         'description': 'Favorite food',
                         'default_option': 'Broccoli',
                         'current_option': 'Ice Cream',
                         'options': "[Pizza, Steak, Ice Cream, Broccoli]",
                         }
        datas = [data_color, data_res, data_food]
        
        nopts = len(sections)
        
        settings = Settings.Settings(filename)
        for i in xrange(nopts):
            setting_name = sections[i]
            data = datas[i]
            opts = Util.Formatting.str_to_struct(data['options'], str)
            di = opts.index(data['default_option'])
            ci = opts.index(data['current_option'])
            setting = Settings.Setting(name=setting_name, description=data['description'],
                                       default_index=di, current_index=ci, options=opts)
            settings.add_setting(setting_name, setting)
        
        settings.save()
        
        #Relying on load working here, but we test that above, so it's cool?
        same_settings = Settings.Settings(filename)
        same_settings.load()
        
        opts1 = settings.settings
        opts2 = same_settings.settings
        for i in xrange(nopts):
            opt1 = opts1[i]
            opt2 = opts2[i]
            self.assertEqual(opt1.description, opt2.description)
            self.assertEqual(opt1.default_option, opt2.default_option)
            self.assertEqual(opt1.current_option, opt2.current_option)
            self.assertEqual(opt1.name, opt2.name)
            self.assertEqual(opt1.options, opt2.options)
        
        import os
        try:
            os.remove(filename)
        except WindowsError:
            pass
        
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
        new_color = "Brown"
        old_len = self.settings["ColorSetting"].nopts
        self.settings.add_option("ColorSetting", new_color)
        new_len = self.settings["ColorSetting"].nopts
        expected = 1
        actual = new_len - old_len
        self.assertEqual(expected, actual)
        
        #Test adding to a non-existant key fails
        with self.assertRaises(KeyError):
            self.settings.add_option("This_Key_Isnt_Real", "a monkey")
        
    def test_remove_option(self):
        old_len = self.settings["ColorSetting"].nopts
        self.settings.remove_option("ColorSetting", "Red")
        new_len = self.settings["ColorSetting"].nopts
        expected = -1
        actual = new_len - old_len
        self.assertEqual(expected, actual)
        
        #Test adding to a non-existant key fails
        with self.assertRaises(KeyError):
            self.settings.remove_option("This_Key_Isnt_Real", "a monkey")

def suite():
    test_suite = unittest.TestSuite()
    suite1 = unittest.makeSuite(SettingTest)
    suite2 = unittest.makeSuite(SettingsTest)
    test_suite.addTests([suite1, suite2])
    return test_suite
    
def load_tests():
    return suite()