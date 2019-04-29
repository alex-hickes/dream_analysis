import pdb

class InputOutput:
    CACHE_MODE = False
    #CACHE_MODE = True
    #INPUT_CACHE_DATA_USER = ["This is Alex here. How are you?", "I rode through the dessert on a horse with no name", "It felt good to be out of the rain", "no", "no", "get analysis", "In the dessert, you can't remember your name", "Because there aint no one to give you no shame."]

    INPUT_CACHE_DATA_USER = ["This is Alex here. How are you?", "I rode through the dessert on a horse with no name", "It felt good to be out of the rain", "no", "no", "new dream", "In the dessert, you can't remember your car", "Because there aint no beautiful to give you no shame.", "no", "no"]


    INTERFACE_TYPE_SIMPLE = "simple"
    INTERFACE_TYPE_KIVY = "kivy"
    INTERFACE_TYPE_HTML5 = "html5"
    DEFAULT_PROMPT = "analysis>"

    def __init__(self, interface_type: str = INTERFACE_TYPE_SIMPLE):
        self.interface_type = interface_type
        self.i = -1

    def read_message(self, prompt=DEFAULT_PROMPT):

        if InputOutput.CACHE_MODE:
            self.i += 1
            print("User> " + InputOutput.INPUT_CACHE_DATA_USER[self.i])
            return InputOutput.INPUT_CACHE_DATA_USER[self.i]

        if self.interface_type == InputOutput.INTERFACE_TYPE_SIMPLE:

            user_msg = input("{} ".format(prompt))
            return user_msg

        if self.interface_type == InputOutput.INTERFACE_TYPE_KIVY:
            raise Exception("Not implemented yet")

    def write_message(self, message, prompt=DEFAULT_PROMPT):

        if InputOutput.CACHE_MODE:
            print("Therapist> " + message)
            return message

        if self.interface_type == InputOutput.INTERFACE_TYPE_SIMPLE:
            print("\n{} {}".format(prompt, message))
            return True

        if self.interface_type == InputOutput.INTERFACE_TYPE_KIVY:
            #TODO: write message to ChatPageScreen via calling message_write.
            raise Exception("Not implemented yet")

        return False
