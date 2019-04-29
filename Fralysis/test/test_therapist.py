from spacy.tokens import Doc
from Fralysis.Client import Client
from Fralysis.Interview import Interview
from Fralysis.Therapist import Therapist
from Fralysis.InputOutput import InputOutput
from Fralysis.Dream import Subject
from Fralysis.Constants import *

def test_therapist_get_name():

    in_out = InputOutput(interface_type=InputOutput.DEFAULT_PROMPT)

    therapist = Therapist(in_out = in_out)

    therapist.start_therapy()

    assert therapist.client.get_name() == "Alex"

    #assert therapist.client.get_dream() is None

def test_therapist_get_dream():

    in_out = InputOutput(interface_type=InputOutput.CACHE_MODE)

    therapist = Therapist(in_out = in_out)

    therapist.start_therapy()

    assert therapist.client.get_name() == "Alex"

    assert therapist.client.get_dream() is not None

    assert therapist.client.get_dream().get_subject() == Subject.CLIENT

    assert therapist.client.get_dream().get_topics() == [Topic.PARENTS]

    assert therapist.client.get_dream().get_ratings() == [Rating.POSITIVE]

    assert therapist.client.get_dream().get_direct_object() == "Horse"

def test_therapist_get_2_dreams():

    in_out = InputOutput(interface_type=InputOutput.CACHE_MODE)

    therapist = Therapist(in_out = in_out)

    therapist.start_therapy()
