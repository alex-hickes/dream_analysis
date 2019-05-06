import sys
from time import sleep
import threading
from enum import Enum

#kivy imports.
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.properties import ListProperty
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.core.audio import SoundLoader
from kivy.properties import ObjectProperty
from kivy.uix.listview import ListItemButton

#Logic import.
#from Fralysis.StartTherapySession import StartTherapySession
from Fralysis.Therapist import Therapist

#Class to control Homepage.
class HomePageScreen(Screen):

    """
    Class to show Fralysis homepage screen
    """

    #Method to confirm exit when leavin application.
    def on_pre_enter(self):
        Window.bind(on_request_close=self.confirmation)

    #Method to Confirm exit.
    def confirmation(self, *args, **kwargs):
        #global popSound
        #popSound.play()
        self.export_to_png('Menu.png')

        box = BoxLayout(orientation='vertical', padding=10, spacing=10)
        buttons = BoxLayout(padding=10, spacing=10)
        pop = Popup(title='Sure?', content=box, size_hint=(None, None), size=(150,150))
        yes = CustButton(text='Yes', on_release=App.get_running_app().stop)
        no = CustButton(text='No', on_release=pop.dismiss)

        buttons.add_widget(yes)
        buttons.add_widget(no)

        attention = Image(source='freud.png')

        box.add_widget(attention)
        box.add_widget(buttons)

        animText = Animation(color=(0,0,0,1)) + Animation(color=(1,1,1,1))
        animText.repeat = True
        animText.start(yes)
        anim = Animation(size=(300,180), duration=0.2, t='out_back')
        anim.start(pop)
        pop.open()
        return True

#Class to create buttons.
class CustButton(ButtonBehavior, Label):

    """
    Class to define custom rounded buttons
    """

    col = ListProperty([0.1, 0.5, 0.7, 1])
    col2 = ListProperty([0.1, 0.1, 0.1, 1])

    def __init__(self, **kwargs):
        super(CustButton, self).__init__(**kwargs)
        self.update()

    def on_pos(self, *args):
        self.update()

    def on_size(self, *args):
        self.update()

    def on_press(self, *args):
        self.update()

    def on_release(self, *args):
        self.col, self.col2 = self.col2, self.col

    def on_color(self, *args):
        self.update()

    def update(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(rgba=self.col)
            Ellipse(size=(self.height, self.height), pos=self.pos)
            Ellipse(size=(self.height, self.height), pos=(self.x + self.width - self.height, self.y))
            Rectangle(size=(self.width-self.height, self.height), pos=(self.x + self.height / 2.0, self.y))

            #Toyota fantasy

class DreamDictScreen(Screen):
    """
    Class to show the Dream model screen
    """

    dreamDicts = []
    path = ''

    def on_pre_enter(self):
        self.ids.box.clear_widgets()
        self.loadData()
        Window.bind(on_keyboard=self.back)
        for dreamDict in self.dreamDicts:
            self.ids.box.add_widget(DreamDict(text=dreamDict))

    def back(self, window, key, *args):
        if key == 27:
            return True

    def on_pre_leave(self):
        Window.unbind(on_keyboard=self.back)

    def loadData(self, *args):
        try:
            with open(self.path + 'data.json', 'r') as data:
                json.dump(self.dreamDicts, data)
        except FileNotFoundError:
            pass

    def saveData(self, *args):
        with open(self.path + 'data.json', 'w') as data:
            json.dump(self.dreamDicts, data)

    def removeWidget(self, dreamDict):
        #global popSound
        #popSound.play()
        textMsg = dreamDict.ids.label.text
        self.ids.box.remove_widget(dreamDict)
        self.dreamDicts.remove(textMsg)
        self.saveData()

    def addWidget(self):
        #global poppapSound
        #poppapSound.play()
        textMsg = self.ids.textMsg.text
        self.ids.box.add_widget(DreamDict(text=textMsg))
        self.ids.textMsg.text = ''
        self.dreamDicts.append(textMsg)
        self.saveData()

class DreamDict(BoxLayout):

    """
    Class to represent a message
    """

    def __init__(self, text='', **kwargs):
        super(DreamDict,self).__init__(**kwargs)
        self.ids.icon.text = text.split(" ", 1)[0]
        self.ids.label.text = text.split(" ", 1)[1]

        if "Therapist" in text:
            #self.add_widget(Image(source='freud.png'))
            #self.ids.icon.source = 'freud.png'
            print("Therapist in text. text = {}".format(text.split()))

class ChatPageScreen(Screen):

    """
    Class to show the chatbot screen
    """

    def on_pre_enter(self, **kwargs):

        super(ChatPageScreen, self).__init__(**kwargs)

        self.my_input = self.ids.textMsg

        self.my_output = self.ids.box

        self.thread = InputOutputGui(self.my_input, self.my_output)

        success = self.thread.start()
        if success:
            return True

    def message(self, messageBox, *args):
        aMsg = self.thread.callback_read(messageBox)

    def get_message(self):
        return self.msg

class ScreenManagement(ScreenManager):

    """
    Class to allow KIVY to manage screens
    """

    pass

class InputOutputGui(threading.Thread):

    """
    Thread to parse data between view and controller
    """

    DEFAULT_PROMPT = "action"

    def __init__(self, input_widget, output_widget):
        super(InputOutputGui, self).__init__()
        self.input_widget = input_widget
        self.output_widget = output_widget
        self.msg = ""
        self.finish = False

        self.therapist = Therapist(in_out=self)

    def stop(self):
        sys.exit()
        #raise Exception("thread stopping...")

    def run(self):
        print("InputOutputGui is Running!")
        self.therapist.start_therapy()

    def callback_read(self, instance=None):
        if instance is None:
            raise Exception("callback invoked but instance is None!")



# Ext 1208 - switchboard forbasingstoke orthopedis. Call to confirm Wexham operation



        self.msg = instance.text
        #self.msg = instance
        self.output_widget.add_widget(DreamDict("User {}".format(instance.text)))
        instance.text = ""

        if "bye" in self.msg.lower():
            self.finish = True

        print("callback_read> {}".format(self.msg))

    def read_message(self, prompt=DEFAULT_PROMPT):
        if self.finish:
            self.stop()

        print("read_message.{}> {}".format(prompt, self.msg))
        count = 0
        while self.msg is None or self.msg == "":
            count += 1
            print("read_message.sleeping")
            sleep(2)
            if count > 10:
                self.stop()

        message = self.msg
        self.msg = ""
        return(message)

    def write_message(self, message, prompt=DEFAULT_PROMPT):
        print("write_message.{}> {}".format(prompt, message))
        self.output_widget.add_widget(DreamDict("Therapist {}".format(message)))
        sleep(3)



class MainApp(App):

    """
    Main method to initialise Graphical User Interface
    """

    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)

    # def build(self):
    #     #return MyDumbScreen()
    #     return ScreenManagement()

    def build(self):
        return ScreenManagement()


"""
    To run:
    > python -m Fralysis.InputOutputGui
"""
if __name__ == '__main__':

    MainApp().run()



# class MainApp(App):
#     def build(self):
#         return ScreenManagement()

#popSound = SoundLoader.load('pop.mp3')
#poppapSound = SoundLoader.load('poppap.mp3')

# if __name__ == "__main__":
#    MainApp().run()
