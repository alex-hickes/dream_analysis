from spacy.tokens import Doc
from Fralysis.Client import Client
from Fralysis.Interview import Interview
from Fralysis.Therapist import Therapist
from Fralysis.InputOutput import InputOutput
from Fralysis.Dream import Subject
from Fralysis.Constants import *

def test_therapist_get_name():
    InputOutput.CACHE_MODE = True
    InputOutput.INPUT_CACHE_DATA_USER = "This is Alex here. How are you?"

    in_out = InputOutput(interface_type=InputOutput.DEFAULT_PROMPT)

    therapist = Therapist(in_out=in_out)

    therapist.start_therapy()

    assert therapist.client.get_name() == "Alex"

    #assert therapist.client.get_dream() is None


def test_therapist_get_dream():

    InputOutput.CACHE_MODE = True
    InputOutput.INPUT_CACHE_DATA_USER = [
        "This is Alex here. How are you?",
        "I rode through the dessert on a horse with no name",
        "It felt good to be out of the rain",
        "no",
        "new dream",
        "In the dessert, you can't remember your car",
        "Because there aint no one to give you no shame.",
        "nothing",
        "get analysis"
    ]

    in_out = InputOutput(interface_type=InputOutput.CACHE_MODE)


    therapist = Therapist(in_out=in_out)

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

def test_sample_dream_one():
    InputOutput.CACHE_MODE = True
    InputOutput.INPUT_CACHE_DATA_USER = [
        "Hi",
        "My name is Sam",
        "I was cycling around Brighton. A red car started chasing me. It hit me. A man got out. It turned out to be my father.",
        "our current relationship is not great",
        "It was dark when this happened",
        "get analysis"
    ]

    in_out = InputOutput(interface_type=InputOutput.CACHE_MODE)

    therapist = Therapist(in_out=in_out)

    therapist.start_therapy()

    assert therapist.client.get_name() == "Sam"

    assert therapist.client.get_dream().get_subject() == Subject.CLIENT
    assert therapist.client.get_dream().get_topics() == [Topic.PSYCHE, Topic.SEX_SYMBOL, Topic.OEDIPUS_COMPLEX]
    assert therapist.client.get_dream().get_ratings() == [Rating.NEGATIVE]
    assert therapist.client.get_dream().get_direct_object() == "Father"

def test_sample_dream_two():
    InputOutput.CACHE_MODE = True
    InputOutput.INPUT_CACHE_DATA_USER = [
        "Hi Siggy",
        "I am Hannah",
        "she had a dream about going on a journey with a friend. As we left, a really bad storm hit.",
        "It was supposed to be fun but took a dark turn",
        "new dream",
        "I took a trip to the beach with my family. Mum and dad had a big argument",
        "Everything was good until then",
        "nope",
        "get analysis"
    ]

    in_out = InputOutput(interface_type=InputOutput.CACHE_MODE)

    therapist = Therapist(in_out=in_out)

    therapist.start_therapy()

    assert therapist.client.get_name() == "Hannah"

    assert therapist.client.get_dream().get_subject() == Subject.SOMEONE
    assert therapist.client.get_dream().get_topics() == [Topic.DEATH, Topic.PSYCHE]
    assert therapist.client.get_dream().get_ratings() == [Rating.VERY_NEGATIVE, Rating.NEGATIVE]
    assert therapist.client.get_dream().get_direct_object() == "Storm"

    assert therapist.client.get_dream(1).get_subject() == Subject.CLIENT
    assert therapist.client.get_dream(1).get_topics() == [Topic.DEATH, Topic.PSYCHE, Topic.OEDIPUS_COMPLEX]
    assert therapist.client.get_dream(1).get_ratings() == [Rating.POSITIVE]
    assert therapist.client.get_dream(1).get_direct_object() == "Dad"

def test_sample_dream_three():
    InputOutput.CACHE_MODE = True
    InputOutput.INPUT_CACHE_DATA_USER = [
        "Hi",
        "It's Chris here",
        "She is going through the hall of her house and strikes her head against the low-hanging chandelier, so that her head bleeds",
        "It was my friends house",
        "It was darker than usual",
        "not much else i remember",
        "no",
        "new dream",
        "I was walking past a mansion and a naked person was lying in the sun.",
        "I remember the weather being nice. She was rather beautiful",
        "not really",
        "no!",
        "get analysis"
    ]

    in_out = InputOutput(interface_type=InputOutput.CACHE_MODE)

    therapist = Therapist(in_out=in_out)

    therapist.start_therapy()

    assert therapist.client.get_name() == "Chris"

    assert therapist.client.get_dream().get_subject() == Subject.SOMEONE
    assert therapist.client.get_dream().get_topics() == [Topic.BODY]
    assert therapist.client.get_dream().get_ratings() == [Rating.NEGATIVE]
    assert therapist.client.get_dream().get_direct_object() == "House"

    assert therapist.client.get_dream(1).get_subject() == Subject.CLIENT
    assert therapist.client.get_dream(1).get_topics() == [Topic.BODY]
    assert therapist.client.get_dream(1).get_ratings() == [Rating.POSITIVE, Rating.POSITIVE]
    assert therapist.client.get_dream(1).get_direct_object() == "Naked"

def test_sample_dream_four():
    InputOutput.CACHE_MODE = True
    InputOutput.INPUT_CACHE_DATA_USER = [
        "I am Warrick. How are you?",
        "She is standing in front of the drawer of her writing table, with which she is so familiar that she knows immediately if anybody has been through it",
        "It was comforting",
        "no",
        "no",
        "new dream",
        "I was walking through the street and a load of naked people started chasing me.",
        "It was a weird. Ultimately fun, I guess",
        "That does it"
        "Fuck off!",
        "get analysis"
    ]

    in_out = InputOutput(interface_type=InputOutput.CACHE_MODE)

    therapist = Therapist(in_out=in_out)

    therapist.start_therapy()

    assert therapist.client.get_name() == "Warrick"

    assert therapist.client.get_dream().get_subject() == Subject.SOMEONE
    assert therapist.client.get_dream().get_topics() == [Topic.OEDIPUS_COMPLEX]
    assert therapist.client.get_dream().get_ratings() == [Rating.POSITIVE]
    assert therapist.client.get_dream().get_direct_object() == "Table"

    assert therapist.client.get_dream(1).get_subject() == Subject.CLIENT
    assert therapist.client.get_dream(1).get_topics() == [Topic.BODY, Topic.PSYCHE]
    assert therapist.client.get_dream(1).get_ratings() == [Rating.POSITIVE]
    assert therapist.client.get_dream(1).get_direct_object() == "Chase"

def test_sample_dream_five():
    InputOutput.CACHE_MODE = True
    InputOutput.INPUT_CACHE_DATA_USER = [
        "Hi. My name is blah",
        "It's actually Sarah",
        "Someone broke into my house. They were dressed in black. I chased him and he ran into the darkness.",
        "It was scary and spooky",
        "no",
        "nope",
        "new dream",
        "I am sitting in a train and it goes through all these beautiful places, from mountains to fields",
        "very good",
        "no",
        "All good Siggy",
        "get analysis"
    ]

    in_out = InputOutput(interface_type=InputOutput.CACHE_MODE)

    therapist = Therapist(in_out=in_out)

    therapist.start_therapy()

    assert therapist.client.get_name() == "Sarah"

    assert therapist.client.get_dream().get_subject() == Subject.SOMEONE
    assert therapist.client.get_dream().get_topics() == [Topic.BODY, Topic.PSYCHE]
    assert therapist.client.get_dream().get_ratings() == [Rating.VERY_NEGATIVE, Rating.NEGATIVE]
    assert therapist.client.get_dream().get_direct_object() == "Chase"

    assert therapist.client.get_dream(1).get_subject() == Subject.CLIENT
    assert therapist.client.get_dream(1).get_topics() == [Topic.SEX_SYMBOL, Topic.PSYCHE]
    assert therapist.client.get_dream(1).get_ratings() == [Rating.POSITIVE]
    assert therapist.client.get_dream(1).get_direct_object() == "Field"