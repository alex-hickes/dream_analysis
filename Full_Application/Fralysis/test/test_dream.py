from Fralysis.SpacySetup import *
from Fralysis.test.test_data import *
from Fralysis.MessageTypeAnalysis import MessageTypeAnalysis
from Fralysis.Dream import *
from Fralysis.AnalyseDream import *
from Fralysis.DreamValidator import *

def test_dream_message():

    #An Input which contains a dream
    for message in VALID_DREAMS:

        # message_nlp as processed by messageTypeAnalysis
        message_nlp = MessageTypeAnalysis(message).is_dream()

        #Create a dream
        a_dream = Dream(message_nlp)

        #Test the contents of the dream match the message provided by user
        assert a_dream.get_latest_message() == message_nlp

def test_dream_subject_client():

    #An Input which contains a dream
    message = "I am the subject of the dream"

    # message_nlp as processed by messageTypeAnalysis
    message_nlp = MessageTypeAnalysis(message).is_dream()
    #Create a dream
    a_dream = Dream(message_nlp)

    analyse_dream = AnalyseDream(a_dream)

    assert a_dream.get_subject() == Subject.CLIENT

def test_dream_subject_someone():

    #An Input which contains a dream
    message = "The subject of the dream is a friend"

    # message_nlp as processed by messageTypeAnalysis
    message_nlp = MessageTypeAnalysis(message).is_dream()

    #Create a dream
    a_dream = Dream(message_nlp)

    analyse_dream = AnalyseDream(a_dream)

    assert a_dream.get_subject() == Subject.SOMEONE

def test_dream_subject_other():

    #An Input which contains a dream
    message = "The dream is about my car."

    # message_nlp as processed by messageTypeAnalysis
    message_nlp = MessageTypeAnalysis(message).is_dream()

    #Create a dream
    a_dream = Dream(message_nlp)

    analyse_dream = AnalyseDream(a_dream)

    assert a_dream.get_subject() == Subject.OTHER

def test_dream_dir_obj():

    #An Input which contains a Dream.
    message = VALID_DREAMS[2]

    # message_nlp as processed by MessageTypeAnalysis.
    message_nlp = MessageTypeAnalysis(message).is_dream()

    #Create a Dream.
    a_dream = Dream(message_nlp)

    #Assign features of Dream.
    analyse_dream = AnalyseDream(a_dream)

    assert a_dream.get_direct_object() == "Mountain"

def test_dream_topic():

    #An Input which contains a Dream.
    message = VALID_DREAMS[2]

    # message_nlp as processed by MessageTypeAnalysis.
    message_nlp = MessageTypeAnalysis(message).is_dream()

    #Create a Dream.
    a_dream = Dream(message_nlp)

    #Assign features of Dream.
    analyse_dream = AnalyseDream(a_dream)

    assert a_dream.get_topics() == [Topic.SEX_SYMBOL, Topic.PSYCHE]

def test_dream_rating():

    #An Input which contains a Dream.
    message = VALID_DREAMS[3]

    # message_nlp as processed by MessageTypeAnalysis.
    message_nlp = MessageTypeAnalysis(message).is_dream()

    #Create a Dream.
    a_dream = Dream(message_nlp)

    #Assign features of Dream.
    analyse_dream = AnalyseDream(a_dream)

    assert a_dream.get_ratings() == [Rating.POSITIVE, Rating.POSITIVE]

def test_dream_valid():

    #message = VALID_DREAMS[3]
    #message = VALID_DREAMS[4]
    message = VALID_DREAMS[5]

    # message_nlp as processed by MessageTypeAnalysis.
    message_nlp = MessageTypeAnalysis(message).is_dream()

    #Create a Dream.
    a_dream = Dream(message_nlp)

    #Assign features of Dream.
    analyse_dream = AnalyseDream(a_dream)

    dream_validity = DreamValidator(a_dream)

    print(str(dream_validity.outstanding_features()))

    assert dream_validity.is_valid() == False
