from enum import Enum

DEBUG_ENABLED = False

#Enum for Freudian topics.
class Topic(Enum):
    LIFE_FULFILL = 1
    SEX_SYMBOL = 2
    BIRTH = 3
    BODY = 4
    PARENTS = 5
    CHILDREN = 6
    SIBLINGS = 7
    DEATH = 8
    OEDIPUS_COMPLEX = 9
    PSYCHE = 10

#Enum for descriptive ratings.
class Rating(Enum):
    VERY_NEGATIVE = -3
    NEGATIVE = -2
    SOMEWHAT_NEGATIVE = -1
    NEUTRAL = 0
    SOMEWHAT_POSITIVE = 1
    POSITIVE = 2
    VERY_POSITIVE = 3

#Ranged ratings.
MIN_RATING_VALUE = Rating.VERY_NEGATIVE.value
MAX_RATING_VALUE = Rating.VERY_POSITIVE.value

#Set of words relating to negation.
NEGATIONS = {
    "no",
    "not",
    "none",
    "isn't",
    "wasn't"
}

# _RATING_TO_NEGATED_MAP = {
RATING_TO_NEGATED_MAP = {
    Rating.VERY_NEGATIVE : Rating.SOMEWHAT_POSITIVE,
    Rating.NEGATIVE : Rating.POSITIVE,
    Rating.SOMEWHAT_NEGATIVE : Rating.SOMEWHAT_POSITIVE,
    Rating.SOMEWHAT_POSITIVE : Rating.SOMEWHAT_NEGATIVE,
    Rating.POSITIVE : Rating.NEGATIVE,
    Rating.VERY_POSITIVE : Rating.SOMEWHAT_NEGATIVE,
}

#Set of words which intensiy ratings.
INTENSIFIERS = {
    'really',
    'very',
    'strongly',
    'so',
    'big'
}

#Set of words which diminish ratings.
DIMINISHERS = {
    'slightly',
    'barley',
    'little',
    'somewhat'
}

#Class for classifiying messages irrelevant to dreams.
class Miscellaneous(Enum):
    GREETING = 1
    WEATHER = 2

#Class for classifiying what to do after a dream diagnosis is complete.
class PostOption(Enum):
    MORE_INFO = 1
    NEW_DREAM = 2
    GET_ANALYSIS = 3

#Generic words assciated to miscellaneous greeting terms.
GREETING_TERMS = ["Hello", "Hi", "Good", "Morning", "Evening", "Lovely", "How", "Do", "You", "Do"]
#Responses assciated to miscellaneous greeting terms.
GREETING_RESPONSE = ["Hello, how can I help you?", "Hi there! How can I be of assistance today?"]

WEATHER_TERMS = ["Weather", "Day"]

WEATHER_RESPONSE = ["Hi, what a lovely day.", "How about this weather huh?"]

VALID_NAME_LIST = ["Warrick"]

#Words which mistakenly defined as propnoun.
NOT_NAMES = ["I", "I'm", "Am", "Hello", "Hi", "My", "Name", "My Name", "Is", "Siggy", "Good", "Evening", "Morning", "Day", "Mr", "Mrs", "Miss", "Dr"]

#Therapist messages: Ask for name

INTRODUCTION_MESSAGE = [
    "Hi!",
    "Hello!",
    "Hi, nice to meet you.",
    "Hi there! Thanks for stopping by.",
    "Ahh, you caught me off guard! Come on in."
]

REQUEST_NAME = [
    "My name is Siggy, what is yours?",
    "Can you tell me your name please?",
    "In order to begin, I need to get your name.",
    "Lets see if you're been here before. Whats your name?"
]

FIRST_GREETING = [
    "Hi {}, great to meet you.",
    "{}, what a great name.",
    "My pleasure to meet you {}.",
    "Well {}, thank you for coming.",
    "Brilliant! Shall we get started, {}?"
]

REPEAT_REQUEST_NAME = [
    "Sorry, I didn't catch your name?",
    "Did you tell me your name?",
    "Apologies, but I can't seem to interpret that as a name. Try again.",
    "Come again?",
    "Really? Was that REALLY your name?"
]

URGENT_REQUEST_NAME = [
    "I really need your name please.",
    "Could you repeat your name please, I missed it?",
    "Unfortunatley, this session cannot continue if you do not provide me with your name.",
    "Nope, still didn't get that. One last try.",
    "This is the last time. What's your name friend?"
]

NO_NAME_GIVEN = [
    "Sorry, I can not continue if you will not tell me your name.",
    "Unfortunatley, I haven't been able to recognise your name. Good bye.",
    "Maybe I'm having a bad day, but we can't continue if you do not give me your name. Maybe next time.",
    "Hmmm, maybe we should continue this when you want to tell me your name."
]




MORE_INFO_RESPONSE = ["provide more info", "give info", "get more info", "more info"]

NEW_DREAM_RESPONSE = ["new dream", "get another dream", "provide new dream"]

GET_ANALYSIS_RESPONSE = ["get analysis"]


POS_SUBJECTS = [
    "i", "i'm", "me", "someone", "he", "him", "his", "she", "her", "friend", "parent", "mum", "mother", "dad", "father", "brother", "sister", "uncle", "aunt", "the", "it"]

POS_CLIENT_SUBJECTS = [
    "i", "i'm", "me"]

POS_SOMEONE_SUBJECTS = [
    "he", "him", "his", "she", "her", "friend", "someone", "parent", "mum", "mother", "dad", "father", "brother", "sister", "uncle", "aunt"]

POS_OTHER_SUBJECTS = [
    "the", "it"]



REQUEST_DREAM = [
    "Alright then! Could you provide some information regarding your dream?",
    "How about you tell me about your dream?",
    "Ok then, Lets get some details about your dream."
]

REPEAT_REQUEST_DREAM = [
    "Seems like that dream doesn't quite cut out. Mind trying again?",
    "Still didn't get that. Tell me a bit about your dream.",
    "Come again?"
]

URGENT_REQUEST_DREAM = [
    "Seriously now, I need some sort of dream",
    "Com'on buster, quit playing around. WHats your dream.",
    "This is the last chance to give me any information about your dream."
]

NO_DREAM_GIVEN = [
    "Sorry, can't complete analysis as dream is still incomplete."
]

DREAM_COLLECTED = [
    "Brilliant! I think I have enough information to analyse your dream!",
    "That should be enough, lets see what this all means."
]

MORE_INFO_SUBJECT = [
    "Is there any more details you wish to provide regarding the subject?",
    "What else can you tell me about the subject of this dream?"
]

MORE_INFO_TOPIC = [
    "Is there any more details you could provide about the main players in the dream?",
    "Tell me about the main feature of your dream?"
]

MORE_INFO_RATNG = [
    "Is there any more details you wish to provide regarding the context?",
    "What more can you tell me about the emotion of the dream?"
]



REQUEST_SUBJECT = [
    "Tell me about who or what this dream is about?",
    "Who or what is the main subject of this dream?"
]

REPEAT_REQUEST_SUBJECT = [
    "Sorry, I didn't catch that. What is the subject?",
    "Did you tell me the dream subject?"
]

URGENT_REQUEST_SUBJECT = [
    "I really need the subject to continue",
    "Could you repeat the subject please, I missed it?"
]

NO_SUBJECT_GIVEN = [
    "Sorry, I can not give meaning to the dream without a subject."
]

CLIENT_SUBJECT_RESPONSE = [
    "Ahh! So this dream is about you then.",
    "So you're the main subject",
    "Brilliant! Lets continue."
]

SOMEONE_SUBJECT_RESPONSE = [
    "So the main subject is a friend of yours.",
    "So this dream is about your friend."
]

OTHER_SUBJECT_RESPONSE = [
    "So this dream is about a {}.",
    "Alright, so you were having a dream about your {}"
]



REQUEST_TOPIC = [
    "Tell me about the main features of the dream? How do they make you feel?",
    "What is the main feature that exists in this dream?",
    "What thing has the greatest impact on your dream?"
]

REPEAT_REQUEST_TOPIC = [
    "Sorry, I didn't catch that. Who or what is influencing your dream?",
    "Did you tell me what the dream is about?"
]

URGENT_REQUEST_TOPIC = [
    "I really need something that is the main object of the dream",
    "Could you repeat that please, I missed it?"
]

NO_TOPIC_GIVEN = [
    "Sorry, I can not give meaning to the dream without a central subject."
]

TOPIC_RESPONSE = [
    "Brilliant, I've made a note of that.",
    "Fantastic! Looks like I've found something there."
]



REQUEST_RATING = [
    # "Could you provide a some context to this dream. How did it make you feel?",
    # "What is the main emotion of this dream?"
    "How did the {} appear in this dream?",
    "Can you tell me more about the {}?"
]

REPEAT_REQUEST_RATING = [
    "Sorry, I didn't catch that. How does that make you feel?",
    "Did you tell me the context of the dream?"
]

URGENT_REQUEST_RATING = [
    "I really need the context to give meaning to your dream",
    "Could you repeat that please, I missed it?"
]

NO_RATING_GIVEN = [
    "Sorry, I can not give meaning to the dream without some kind of emotion."
]

RATING_RESPONSE = [
    "Brilliant, I've made a note of that.",
    "Hmm ok. Interesting. Lets continue"
]

FINAL_INFO = [
    "What you've said looks good. Anything else you wish to add?"
]

FINAL_INFO_RESP = [
    "Brilliant, I've made a note of that.",
    "Sure. Well, lets get to the fun bit."
]

REQUEST_POST_ANALYSIS_OPTION = [
    "Seems like I've deducted a meaning for your dream. But before we analysis, would you like to 'get analysis' or provide a 'new dream'?",
    "Before I interpret your dream, would you like to 'get analysis' or provide a 'new dream'?",
    "Would you like to.. A) Provide 'new dream' B) 'get analyse'"
]

NO_OPTION = ["Sorry, didn't catch that. again. Would you like to : 'get analysis' or give a 'new dream'."]


EVEN_MORE_INFO = [
    "Is that it?"
]
NO_MORE_INFO = [
    "no",
    "not really",
    "nope",
    "na",
    "do",
    "that should do",
    "done"
]

MORE_INFO = [
    "yes",
    "ye"
]


REQUEST_ANOTHER_DREAM = [
    "Sure.",
    "Lets see what similarities we can find?"
    "You can give as many dreams as ou want. Go for it!"
]

CREATE_CLIENT_CONTEXT_RESPONSE = "The dream you have given me seems to effect you in a {} context."

CREATE_SOMEONE_CONTEXT_RESPONSE = "The dream you have given me seems to have a {} context for someone you know."

CREATE_OTHER_CONTEXT_RESPONSE =  "The dream you have given has a {} context."

CREATE_RESPONSE = "{} Features of your dream relate to freudian features including {}. {}"
