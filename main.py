import os
from threading import Thread
from time import sleep



from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.animation import Animation

from pidev.MixPanel import MixPanel
from pidev.kivy.PassCodeScreen import PassCodeScreen
from pidev.kivy.PauseScreen import PauseScreen
from pidev.Joystick import Joystick
from pidev.kivy import DPEAButton
from pidev.kivy import ImageButton
import random
MIXPANEL_TOKEN = "x"
MIXPANEL = MixPanel("Project Name", MIXPANEL_TOKEN)

SCREEN_MANAGER = ScreenManager()
MAIN_SCREEN_NAME = 'main'
ADMIN_SCREEN_NAME = 'admin'
SKY_SCREEN_NAME = 'SideScreen'
JOY_SCREEN_NAME = 'joyScreen'


class ProjectNameGUI(App):
    """
    Class to handle running the GUI Application
    """

    def build(self):
        """
        Build the application
        :return: Kivy Screen Manager instance
        """
        return SCREEN_MANAGER


Window.clearcolor = (0, 0, 0.1, 100)  # White

xy = property(None)
btn6 = property(None)
lb0 = property(None)
lbz = property(None)

class JoyScreen(Screen):
    joystick = Joystick(0, False)
    X_axis = ObjectProperty(0.0)
    Y_axis = ObjectProperty(0.0)


    def __init__(self, **kwargs):
        Builder.load_file('joyScreen')
        super(JoyScreen, self).__init__(**kwargs)

    def switch_text2(self):
        list = [1]

        if self.joystick.button_combo_check(list)==1:
            self.lbz.text = ""
            self.lb0.text = "Ready"
            self.xy.color = 0, 1, 0, 1

            if self.joystick.get_button_state(0) == 0:
                self.lb0.text = "Ready"
                self.xy.color = 0, 1, 0, 1
            else:
                self.lb0.text = ""
                self.xy.color = 1, 0, 0, 1
                self.counter()

        else:
            self.lbz.text = "Hold 2"
            self.lb0.text = ""
            self.xy.color = 1, 1, 1, 1


    def joystick_thread(self):
        while 1:
            self.joystick.refresh()
            self.X_axis = self.joystick.get_axis('x') * Window.size[0] * 1/2
            self.Y_axis = self.joystick.get_axis('y') * Window.size[1] * 1/2
            # self.switch_text()
            self.switch_text2()
            sleep(1/200)
            # print(self.X_axis)

    def start_joystick_thread(self):
        Thread(target=self.joystick_thread).start()

    def transition_back(self):
        """
        Transition back to the main screen
        :return:
        """
        SCREEN_MANAGER.current = MAIN_SCREEN_NAME

    global xin
    xin = 0
    global x

    def counter(self):
        global xin
        global x
        xin = xin + 1
        if xin == 1000:
            xin = 0
        else:
            print ("%d" % xin)
            x = "%d" % xin
            random.seed(x)
            Window.clearcolor = (random.random(), random.random(), random.random(), 1000)






test_button3 = property(None)
fly2 = property(None)

class SideScreen(Screen):
    def __init__(self, **kwargs):
        Builder.load_file('sideScreen.kv')
        super(SideScreen, self).__init__(**kwargs)
        anim = Animation(x=50) + Animation(size=(180, 80)) + Animation(x=90) + Animation(size=(150, 150)) + Animation(
            y=50) + Animation(y=150)
        anim.repeat = True
        anim.start(self.fly2)

    def transition_back(self):
        """
        Transition back to the main screen
        :return:
        """
        SCREEN_MANAGER.current = MAIN_SCREEN_NAME

    def exit_program(self):
        """
        Quit the program. This should free all steppers and do any cleanup necessary
        :return: None
        """
        quit()

    def random(self):
        if self.test_button3.text == "o-\<":
            self.test_button3.text = "o-/<"

        elif self.test_button3.text == "o-/<":
            self.test_button3.text = "o-\<"


class MainScreen(Screen):
    """
    Class to handle the main screen and its associated touch events
    """

    btn1 = property(None)
    btn2 = property(None)
    btn3 = property(None)
    fly = property(None)

    def __init__(self, **kwargs):
        Builder.load_file('sideScreen.kv')
        super(MainScreen, self).__init__(**kwargs)
        anim = Animation(x=50) + Animation(size=(80, 80)) + Animation(x=90) + Animation(size=(150, 150)) + Animation(y=50) + Animation(y=100)
        anim.repeat = True
        anim.start(self.fly)


    def next(self):
        SCREEN_MANAGER.current = SKY_SCREEN_NAME

    def next2(self):
        SCREEN_MANAGER.current = JOY_SCREEN_NAME
    def affect(self):
        self.btn3.text = "Changing..."
        if self.lb1.text == "Motor On":
            self.lb1.text = "Motor Off"

        elif self.lb1.text == "Motor Off":
            self.lb1.text = "Motor On"
    def switch_text(self):

        if self.btn1.text == "On":
            self.btn1.text = "Off"

        elif self.btn1.text == "Off":
            self.btn1.text = "On"

    global xin
    xin = 0
    def counter(self):
        global xin
        xin = xin + 1
        self.btn2.text = "%d" % xin





    def pressed(self):
        """
        Function called on button touch event for button with id: testButton
        :return: None
        """
        PauseScreen.pause(pause_scene_name='pauseScene', transition_back_scene='main', text="Test", pause_duration=5)

    def admin_action(self):
        """
        Hidden admin button touch event. Transitions to passCodeScreen.
        This method is called from pidev/kivy/PassCodeScreen.kv
        :return: None
        """
        SCREEN_MANAGER.current = 'passCode'


class AdminScreen(Screen):
    """
    Class to handle the AdminScreen and its functionality
    """

    def __init__(self, **kwargs):
        """
        Load the AdminScreen.kv file. Set the necessary names of the screens for the PassCodeScreen to transition to.
        Lastly super Screen's __init__
        :param kwargs: Normal kivy.uix.screenmanager.Screen attributes
        """
        Builder.load_file('AdminScreen.kv')

        PassCodeScreen.set_admin_events_screen(ADMIN_SCREEN_NAME)  # Specify screen name to transition to after correct password
        PassCodeScreen.set_transition_back_screen(MAIN_SCREEN_NAME)  # set screen name to transition to if "Back to Game is pressed"

        super(AdminScreen, self).__init__(**kwargs)

    @staticmethod
    def transition_back():
        """
        Transition back to the main screen
        :return:
        """
        SCREEN_MANAGER.current = MAIN_SCREEN_NAME

    @staticmethod
    def shutdown():
        """
        Shutdown the system. This should free all steppers and do any cleanup necessary
        :return: None
        """
        os.system("sudo shutdown now")

    @staticmethod
    def exit_program():
        """
        Quit the program. This should free all steppers and do any cleanup necessary
        :return: None
        """
        quit()
"""
Widget additions
"""

Builder.load_file('main.kv')
SCREEN_MANAGER.add_widget(MainScreen(name=MAIN_SCREEN_NAME))
SCREEN_MANAGER.add_widget(PassCodeScreen(name='passCode'))
SCREEN_MANAGER.add_widget(PauseScreen(name='pauseScene'))
SCREEN_MANAGER.add_widget(AdminScreen(name=ADMIN_SCREEN_NAME))
SCREEN_MANAGER.add_widget(SideScreen(name=SKY_SCREEN_NAME))
SCREEN_MANAGER.add_widget(JoyScreen(name=JOY_SCREEN_NAME))

"""
MixPanel
"""


def send_event(event_name):
    """
    Send an event to MixPanel without properties
    :param event_name: Name of the event
    :return: None
    """
    global MIXPANEL

    MIXPANEL.set_event_name(event_name)
    MIXPANEL.send_event()


if __name__ == "__main__":
    # send_event("Project Initialized")
    # Window.fullscreen = 'auto'
    ProjectNameGUI().run()
