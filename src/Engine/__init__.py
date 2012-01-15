"""
Engine-level util and globals.
ex. ID_Manager is an __id_manager that can be accessed once
the engine has been imported.  This provides a single access
point to the id pool, so there are not id collisions.
"""

import Events
import ID
import Settings
import Util
