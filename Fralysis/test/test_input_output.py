
from Fralysis.InputOutput import InputOutput


def test_send_message():

    message = "This is a test"

    in_out = InputOutput(interface_type=InputOutput.INTERFACE_TYPE_SIMPLE)

    print("this is me testing....\n")

    assert in_out.write_message(message=message)


def test_read_message():

    InputOutput.CACHE_MODE = True
    InputOutput.INPUT_CACHE_DATA = "This is Alex here. How are you?"

    in_out = InputOutput(interface_type=InputOutput.INTERFACE_TYPE_SIMPLE)

    in_out.write_message("Please enter your name.")
    message = in_out.read_message()

    assert message == InputOutput.INPUT_CACHE_DATA

# def test_prompt():
#
#     InputOutput.CACHE_MODE = False
#     in_out = InputOutput(interface_type=InputOutput.INTERFACE_TYPE_SIMPLE)
#
#     in_out.write_message("Please enter your name.")
#     message = in_out.read_message()
#
#     assert message == "John"
