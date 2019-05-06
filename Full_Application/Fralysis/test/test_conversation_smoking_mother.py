from Fralysis.InputOutput import InputOutput
from Fralysis.Therapist import Therapist
from Fralysis.MessageTypeAnalysis import MessageTypeAnalysis
from Fralysis.DreamValidator import Request
from Fralysis.Dream import *
from Fralysis.AnalyseDream import *
from Fralysis.DreamValidator import *

def test_ask_for_name():
    """
    > pytest -s

    :return:
    """

    InputOutput.CACHE_MODE = True
    in_out = InputOutput(interface_type=InputOutput.INTERFACE_TYPE_SIMPLE)

    InputOutput.INPUT_CACHE_DATA_USER = [
        "This is Alex here. How are you?",

    ]

    therapist = Therapist(in_out=in_out)

    assert therapist.interview.ask_for_name()

    print("name: {}".format(therapist.client.get_name()))

    assert therapist.client.get_name() == "Alex"


def test_smoking():
    """
    > pytest -s

    :return:
    """
    #DEBUG_ENABLED = True
    InputOutput.CACHE_MODE = True
    in_out = InputOutput(interface_type=InputOutput.INTERFACE_TYPE_SIMPLE)

    InputOutput.INPUT_CACHE_DATA_USER = "This is Alex here. How are you?"

    therapist = Therapist(in_out=in_out)

    assert therapist.interview.ask_for_name()

    print("name: {}".format(therapist.client.get_name()))

    assert therapist.client.get_name() == "Alex"

    InputOutput.INPUT_CACHE_DATA_USER = "My uncle is smoking a cigarette in a car, although it is Saturday."
    #InputOutput.INPUT_CACHE_DATA_USER = "My uncle is smoking a cigarette, although it is Saturday. A woman caressed me as if I were her child."


    message_for_dream = MessageTypeAnalysis(InputOutput.INPUT_CACHE_DATA_USER).is_dream(Request.SUBJECT)
    a_dream = Dream(message_for_dream)
    AnalyseDream(a_dream)

    assert a_dream.get_subject() == Subject.SOMEONE
    assert a_dream.get_direct_object() == "Car"
    assert a_dream.get_ratings() == [Rating.NEGATIVE]

