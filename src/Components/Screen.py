"""
Screen is a container of elements and components

Screens have states: Active, Hidden, TransitionOn, TransitionOff
Screen have transitions: 1 for fully off, 0 for fully on.
    Transition can be thought of as percent of transition remaining to on.
"""

import Util
from Container import Container

SCREEN_STATES = Util.Structs.enum('TRANSTION_ON', 'ACTIVE',
                         'TRANSITION_OFF', 'HIDDEN')

class Screen(Container):
    """
    A logical grouping of related display items.
    
    Example screens: MainMenuScreen, CreditsScreen, LobbyScreen,
                     GameScreen, SettingsScreen, PauseScreen
    
    Screens have the following states:
    Hidden --> TransitionOn --> Active --> TransitionOff --> Hidden
    States can progress left to right, and transitions can be skipped.
    """
    def __init__(self, window, **kwargs):
        Container.__init__(self, **kwargs)
        
        self._window = window
        self._transition_position = 1.0
        self._exiting = False
        self._state = SCREEN_STATES.TRANSITION_ON
        
        self.TransitionOnTime = 0.0
        self.TransitionOffTime = 0.0
    
    @property
    def Exiting(self):
        """If the screen is in the process of (or about to) exit(ing)."""
        return self._exiting
    
    @property
    def State(self):
        """The screen's current SCREEN_STATE"""
        return self._state
    
    def update_screen(self, dt, other_screen_has_focus, covered_by_other_screen):
        """Updates the screen's transition state and visibility"""
        #Import update code here
        
        #Don't update if no time has passed
        if Util.Math.is_zero(dt):
            return
        self.update(dt)
        
        if self._exiting:
            self._state = SCREEN_STATES.TRANSITION_OFF
            if not self._update_transition(dt, self.TransitionOffTime, 1):
                #Remove the screen when transition finishes
                self.ScreenManager.RemoveScreen(self)
                self._exiting = False
        elif covered_by_other_screen and not self.ForceDraw:
            #If the screen is covered by another,
                #it should transition off
            #UNLESS we are forcing it to draw.
                    #then, this sucker draws whether it wants to or not.
            if self._update_transition(dt, self.TransitionOffTime, 1):
                #Still transitioning
                self._state = SCREEN_STATES.TRANSITION_OFF
            else:
                #Finished transition
                self._state = SCREEN_STATES.HIDDEN
        else:
            #The screen should transition on and be active
            if self._update_transition(dt, self.TransitionOnTime, -1):
                #Still transitioning
                self._state = SCREEN_STATES.TRANSITION_ON
            else:
                #Finished transition
                self._state = SCREEN_STATES.ACTIVE
                
    def _update_transition(self, dt, time, direction): #pylint:disable-msg=C0103,C0301
        """Helper method to update the transition position"""
        pass