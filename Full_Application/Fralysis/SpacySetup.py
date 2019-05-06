import spacy
from spacy.tokens import Token
from enum import Enum
import re
import csv
from math import isclose
from Fralysis.Constants import *

#Method to return negated rating.
def negated_rating(rating: Rating) -> Rating:
    assert rating is not None
    # return _RATING_TO_NEGATED_MAP[rating]
    return RATING_TO_NEGATED_MAP[rating]

#Method to identify negation.
def is_negation(token: Token) -> bool:
    return token.lemma_.lower() in NEGATIONS

#Method to identify an intensifier.
def is_intensifier(token: Token) -> bool:
    return token.lemma_.lower() in INTENSIFIERS

#Method to identify a diminisher.
def is_diminisher(token: Token) -> bool:
    return token.lemma_.lower() in DIMINISHERS

#Method for identifying intensifier/diminisher.
def signum(value) -> int:
    if value > 0:
        return 1
    if value < 0:
        return -1
    else:
        return 0

#Processes range of ratings.
def _ranged_rating(rating_value: int) -> Rating:
    # return Rating(min(_MAX_RATING_VALUE, max(_MIN_RATING_VALUE, rating_value)))
    return Rating(min(MAX_RATING_VALUE, max(MIN_RATING_VALUE, rating_value)))

#Method for decrementing rating if diminisher is present.
def diminished(rating:Rating) -> Rating:
    if abs(rating.value) > 1:
        return _ranged_rating(rating.value - signum(rating.value))
    else:
        return rating

#Method for incrementing rating if intensifier is present.
def intensified(rating:Rating) -> Rating:
    if abs(rating.value) > 1:
        return _ranged_rating(rating.value + signum(rating.value))
    else:
        return rating

#Method to extend spaCy pipeline.
def dream_matcher(doc):
    for sentence in doc.sents:
         for token in sentence:
             if is_diminisher(token):
                 token._.is_diminisher = True
             elif is_intensifier(token):
                 token._.is_intensifier = True
             elif is_negation(token):
                 token._.is_negation = True
             else:
                 lexicon_entry = lexicon.lexicon_entry_for(token)
                 if lexicon_entry is not None:
                     token._.rating = lexicon_entry.rating
                     token._.topic = lexicon_entry.topic
                     token._.description = lexicon_entry.description
    return doc

#Convert .tsv descriptions to Enums.
def enum_check(strToCheck):
    #Topic Enum conversion.
    if strToCheck == Topic.LIFE_FULFILL.name:
        return Topic.LIFE_FULFILL
    if strToCheck == Topic.SEX_SYMBOL.name:
        return Topic.SEX_SYMBOL
    if strToCheck == Topic.BIRTH.name:
        return Topic.BIRTH
    if strToCheck == Topic.BODY.name:
        return Topic.BODY
    if strToCheck == Topic.PARENTS.name:
        return Topic.PARENTS
    if strToCheck == Topic.CHILDREN.name:
        return Topic.CHILDREN
    if strToCheck == Topic.SIBLINGS.name:
        return Topic.SIBLINGS
    if strToCheck == Topic.DEATH.name:
        return Topic.DEATH
    if strToCheck == Topic.OEDIPUS_COMPLEX.name:
        return Topic.OEDIPUS_COMPLEX
    if strToCheck == Topic.PSYCHE.name:
        return Topic.PSYCHE
    #Rating Enum conversion.
    if strToCheck == Rating.VERY_NEGATIVE.name:
        return Rating.VERY_NEGATIVE
    if strToCheck == Rating.NEGATIVE.name:
        return Rating.NEGATIVE
    if strToCheck == Rating.SOMEWHAT_NEGATIVE.name:
        return Rating.SOMEWHAT_NEGATIVE
    if strToCheck == Rating.SOMEWHAT_POSITIVE:
        return Rating.SOMEWHAT_POSITIVE
    if strToCheck == Rating.POSITIVE.name:
        return Rating.POSITIVE
    if strToCheck == Rating.VERY_POSITIVE.name:
        return Rating.VERY_POSITIVE
    return None

#Class for applying relevant information to a word ready to be entered into the lexicon.
class LexiconEntry:

    """
    Common manifest dream object alongside its latent Freudian interpretation
    """

    _IS_REGEX_REGEX = re.compile(r'.*[.+*\[$^\\]')
    #Method to initialise a lexicon entry.
    def __init__(self, lemma: str, topic: Topic, rating: Rating, description: str):

        """
        Initialise entry for Lexicon

        :type lemma: string
        :param lemma: The root of a word representing manifest content

        :type topic: Topic
        :param topic: Freudian symbolism

        :type rating: Rating
        :param rating: Word's sentiment

        :type description: string
        :param description: Freudian latent content

        :type is_regex: boolean
        :param is_regex: Ensure entry is only text

        """

        assert lemma is not None
        self.lemma = lemma
        self._lower_lemma = lemma.lower()
        self.topic = topic
        self.rating = rating
        self.description = description
        self.is_regex = bool(LexiconEntry._IS_REGEX_REGEX.match(self.lemma))
        self.is_regex = re.compile(lemma, re.IGNORECASE) if self.is_regex else None
    #Method to compare token to lexicon entry.
    def matching(self, token: Token) -> float:
        assert token is not None
        result = 0.0
        if self.is_regex:
            if self._regex.match(token.text):
                result = 0.6
            elif self._regex.match(token.lemma_):
                result = 0.5
        else:
            if token.text == self.lemma:
                result = 1.0
            elif token.text.lower() == self.lemma:
                result = 0.9
            elif token.lemma_ == self.lemma:
                result = 0.8
            elif token.lemma_.lower() == self.lemma:
                result = 0.7
        return result
#Method to overwrite lexicon print context.
def __str__(self) -> str:
    result = 'LexiconEntry(%s' % self.lemma
    if self.topic is not None:
        result += ', topic=%s' % self.topic.name
    if self.rating is not None:
        result += ', rating=%s' % self.rating.name
    if self.is_regex:
        result += ', is_regex=%s' % self.is_regex
    result += ')'
    return result

def __repr__(self) -> str:
    return self.__str__()
#Class to manage lexicon (dictionary of Freudian terms).
class Lexicon:

    """
    Dictionary of Freudian topics and adjective ratings.
    A lexicon is compiled from lexicon entries, which are stored in 'lexiconEntries.tsv'
    """

    def __init__(self):
        self.entries: List[LexiconEntry] = []
    #Method to add tokens to lexicon.
    def append(self, lemma: str, topic: Topic, rating: Rating, description: str):
        lexicon_entry = LexiconEntry(lemma, topic, rating, description)
        self.entries.append(lexicon_entry)
    #Method to compare token to lexicon.
    def lexicon_entry_for(self, token: Token) -> LexiconEntry:
        result = None
        lexicon_size = len(self.entries)
        lexicon_entry_index = 0
        best_matching = 0.0
        while lexicon_entry_index < lexicon_size and not isclose(best_matching, 1.0):
            lexicon_entry = self.entries[lexicon_entry_index]
            matching = lexicon_entry.matching(token)
            if matching > best_matching:
                result = lexicon_entry
                best_matching = matching
            lexicon_entry_index += 1
        return result

lexicon = Lexicon()

class SpacySetup:

    """
    Sets up SpaCy's nlp language pipeline
    """

    def __init__(self):

        """
        Initialise nlp language object

        :type main_nlp: Language
        :param main_nlp: SpaCy's pipeline trained on 'en_core_web_sm' and extended to lexicon
        """

        #Small Model - 29 Mb : Not very effective for name recognition.
        #nlp = spacy.load('en_core_web_sm')
        #Large Model - 800+ Mb : Waaaaaaay more effective but could lead to issues when exporting :S
        nlp = spacy.load('en_core_web_sm')

        self.main_nlp = nlp
        if DEBUG_ENABLED:
            print("nlp type: {}".format(type(self.main_nlp)))
        #Extend spaCy Token account for topics and ratings.
        Token.set_extension('topic', default=None, force=True)
        Token.set_extension('description', default=None, force=True)
        Token.set_extension('rating', default=None, force=True)
        Token.set_extension('is_negation', default=False, force=True)
        Token.set_extension('is_intensifier', default=False, force=True)
        Token.set_extension('is_diminisher', default=False, force=True)

        #Add comparator to spaCy pipeline.
        if nlp.has_pipe('dream_matcher'):
            nlp.remove_pipe('dream_matcher')
        nlp.add_pipe(dream_matcher)

        with open("Fralysis/lexiconEntries.tsv") as tsv:
        #with open("lexiconEntries.tsv") as tsv:
            for row in csv.reader(tsv, dialect="excel-tab"):
                if row[1] == 'None':
                    lexicon.append(row[0], None, enum_check(row[2]), None)
                elif row[2] == 'None':
                    lexicon.append(row[0], enum_check(row[1]), None, row[3])
                else:
                    lexicon.append(row[0], enum_check(row[1]), enum_check(row[2]), row[3])

    def get_nlp(self):

        """
        Get nlp object
        """

        return self.main_nlp
