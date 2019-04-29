
#from Fralysis.MessageTypeAnalysis import MessageTypeAnalysis
from Fralysis.MessageTypeAnalysis import *
from Fralysis.test.test_data import *
from Fralysis.InputOutput import InputOutput

def test_init():


    test_message = "dummy message"
    test_analysis = MessageTypeAnalysis(test_message)

    assert test_analysis.message == test_message
    assert test_analysis.message_nlp is None


def test_is_it_a_name():

    for entry in VALID_NAME_PHRASE_LIST:
        test_analysis = MessageTypeAnalysis(entry)
        #assert test_analysis.input_type() == TYPE_NAME
        assert test_analysis.is_name() in VALID_NAME_PHRASE_LIST

    for entry in INVALID_NAME_LIST:
        test_analysis = MessageTypeAnalysis(entry)
        assert test_analysis.is_name() is False


def test_get_name():

    for entry in VALID_NAME_LIST:
        test_analysis = MessageTypeAnalysis(entry)
        assert test_analysis.is_name() == entry.title()

    for entry in INVALID_NAME_LIST:
        test_analysis = MessageTypeAnalysis(entry)
        assert test_analysis.is_name() is False


def test_input_name_and_verify():

    InputOutput.CACHE_MODE = True
    InputOutput.INPUT_CACHE_DATA = "This is Alex here. How are you?"

    in_out = InputOutput(interface_type=InputOutput.INTERFACE_TYPE_SIMPLE)

    in_out.write_message("Please enter your name.")
    message = in_out.read_message()

    test_analysis = MessageTypeAnalysis(message)
    assert test_analysis.is_name() == "Alex"


def test_is_dream():

    message = "A king rode by on a white horse"
    for message in VALID_DREAMS:
        in_out = InputOutput(interface_type=InputOutput.INTERFACE_TYPE_SIMPLE)

        test_analysis = MessageTypeAnalysis(message)
        print(str(type(test_analysis)))
        assert str(test_analysis.is_dream()) == message
