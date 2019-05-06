from spacy.tokens import Doc
from typing import List, Tuple
from Fralysis.Dream import *
from collections import defaultdict
from Fralysis.Constants import *
from statistics import mean
import pdb


#Method to analyse tokens which are relevant to Topic or Rating.
def is_essential(token: Token) -> bool:

    """
    Determine whether a token has a topic or rating, or modifies the rating

    :param token:
    :return bool: Whether token is required for analysis
    """
    return token._.topic is not None \
        or token._.rating is not None \
        or token._.is_diminisher \
        or token._.is_intensifier \
        or token._.is_negation


#Method to find tokens which are relevant to Topic or Rating.
def essential_tokens(tokens):

    """
    Return a list of essential tokens

    :param tokens:
    :return: list of essential tokens
    """

    return [token for token in tokens if is_essential(token)]


#Method to find predecesing modifiers of a rating.
def combine_ratings(tokens):

    """
    Apply any modifying tokens to original adjective rating

    :param tokens:
    :return:
    """

    rating_token_index = next(
        (
            token_index for token_index in range(len(tokens))
            if tokens[token_index]._.rating is not None
        ),
        None
    )

    if rating_token_index is not None:
        original_rating_token = tokens[rating_token_index]
        combined_rating = original_rating_token._.rating
        modifier_token_index = rating_token_index - 1
        modified = True
        while modified and modifier_token_index >= 0:
            modifier_token = tokens[modifier_token_index]
            if is_intensifier(modifier_token):
                combined_rating = intensified(combined_rating)
            elif is_diminisher(modifier_token):
                combined_rating = diminished(combined_rating)
            elif is_negation(modifier_token):
                combined_rating = negated_rating(combined_rating)
            else:
                modified = False
            if modified:
                del tokens[modifier_token_index]
                modifier_token_index -= 1
        original_rating_token._.rating = combined_rating

def match_dreams(dreams: [Dream]):

    """
    Apply any modifying tokens to original adjective rating

    :param dreams:
    :return:
    """

    import itertools

    for a, b in itertools.combinations(dreams, 2):
        if DEBUG_ENABLED:
            print("A : {}, B : {}".format(a.get_messages(), b.get_messages()))
        topic_matches = set(a.get_topics()).intersection(b.get_topics())

        if DEBUG_ENABLED:
            print("Get the average ratings from A and B")
        a_avg_rating = round(mean([rating.value for rating in a.get_ratings()]))

        if DEBUG_ENABLED:
            print("If a/b is positive/negative, save a/b as str = 'pos/neg'")
        if a_avg_rating > 0:
            a = "positive"
        else:
            a = "negative"

        b_avg_rating = round(mean([rating.value for rating in b.get_ratings()]))
        if b_avg_rating > 0:
            b = "positive"
        else:
            b = "negative"

        #rating_matches = set(a.intersection(b))
        if DEBUG_ENABLED:
            print("a/ b have been converted to pos/neg. a = {}. b = {}".format(a, b))
        if a == b:
            rating_matches = a
        else:
            rating_matches = False
        if DEBUG_ENABLED:
            print("matching topics: {} . Matching ratings: {}".format(topic_matches, rating_matches))
        return topic_matches, rating_matches

class AnalyseDream:

    """
    Class which takes a user's message and classifies dream features
    """

    def __init__(self, dream: Dream = None):

        """

        :param dream:
        """

        if DEBUG_ENABLED:
            print("2.2...1 - AnalyseDream object initialised with the dream to analyse. dream = {}".format(dream))
        self.dream = dream
        if self.dream.get_subject() is None:
            if DEBUG_ENABLED:
                print("2.2...2 - Dream doesn't contain a Subject. Subject = {} - set_subject_of_dream()".format(self.dream.get_subject()))
            self.set_subject_of_dream()
            if DEBUG_ENABLED:
                print("2.2...2 - Dream subject is now = {}".format(self.dream.get_subject()))
        if DEBUG_ENABLED:
            print("2.2...3 - Go through all messages in the dream and get an opinion of them - opinions()")
        #self.opinions(self.dream.get_latest_message())
        self.opinions(self.dream.get_latest_message())

        if DEBUG_ENABLED:
            print("2.2...4 - Dream has been Analysed and features found in the message have been identified in the dream - RETURN")

    def set_subject_of_dream(self):

        """
        Set a subject of a dream

        :return:
        """


        if DEBUG_ENABLED:
            print("2.2...2.1 - Go through the dream's latest_message. If tokens relate to a Subject and dream doesn't have a subject set, set subject depending on Subject token - RETURN Subject")
        for sent in self.dream.get_latest_message().sents:
            for token in sent:

                #if (token.text.strip(".").lower() in other_subjects):# and (self.dream.get_subject() is None):
                if (token._.topic is not None):
                    self.dream.set_subject(Subject.OTHER)
                    if DEBUG_ENABLED:
                        print("Subject = {}".format(self.dream.get_subject()))
                    #return self.dream.get_subject()

                if (token.text.strip(".").lower() in POS_CLIENT_SUBJECTS):# and (self.dream.get_subject() is None):
                    self.dream.set_subject(Subject.CLIENT)
                    return self.dream.get_subject()

                if (token.text.strip(".").lower() in POS_SOMEONE_SUBJECTS) and (self.dream.get_subject() is None):
                    self.dream.set_subject(Subject.SOMEONE)
                    if DEBUG_ENABLED:
                        print("Subject = {}".format(self.dream.get_subject()))
                    return self.dream.get_subject()

            if self.dream.get_subject() is not None:
                return self.dream.get_subject()

        if DEBUG_ENABLED:
            print("2.2...2.2 - No token referencing a subject found. Subject = {} - RETURN None".format(self.dream.get_subject()))
        return None

    #Method to identify Topic and Rating of a sentence.
    def topic_rating_dirobj_description_of(self, tokens: List[Token]):

        """
        Identify a direct object of a dream. Attach a symbol. Provide a description

        :param tokens:
        :return:
        """

        opinion_essence = essential_tokens(tokens)
        if DEBUG_ENABLED:
            print("2.2...3.2.1 - essential tokens are  = {}".format(opinion_essence))

        if DEBUG_ENABLED:
            print("2.2...3.2.2 - Combine ratings. This finds a token with a rating. It then changes rating depending of former adverbs. Look to left of essential tokens for associated Diminisher, Intensifier or Negation")
        combine_ratings(opinion_essence)
        if DEBUG_ENABLED:
            print("2.2...3.2.3 - for each token in a document's sentence's essential tokens:")
        for token in opinion_essence:
            if (token._.topic is not None):
                self.dream.set_direct_object(token.lemma_.title())
                if DEBUG_ENABLED:
                    print("2.2...3.2.4 - dream doesn't contain a direct object, so add a direct object. Direct Object = {}".format(self.dream.get_direct_object()))
                if token._.topic not in self.dream.get_topics():
                    self.dream.add_topic(token._.topic)
                if DEBUG_ENABLED:
                    print("2.2...3.2.5 - Token contains Topic. Token = {}. Topic = {}. Add Topic and Description (if not already there) to dream".format(token.text, self.dream.get_topics()))
                if token._.description not in self.dream.get_descriptions():
                    self.dream.add_description(token._.description)
            if (token._.rating is not None):
                self.dream.add_rating(token._.rating)
                if DEBUG_ENABLED:
                    print("2.2...3.2.6 - Token contains Rating. Token = {}. Rating = {}. Add Rating to dream".format(token.text, token._.rating))
        if DEBUG_ENABLED:
            print("2.2...3.2.7 - All Tokens analysed - RETURN")
        return

    #Method to process user message and identify all topics and ratings provided.
    def opinions(self, feedback: Doc):

        """
        Take a users message and get features

        :param feedback:
        :return:
        """

        if DEBUG_ENABLED:
            print("2.2...3.1 - for latest document (feedback = {}) in the dreams list of messages:".format(feedback))
        #for document in feedback:
        for sent in feedback.sents:
            if DEBUG_ENABLED:
                print("2.2...3.2 - for each token in a document's sentence: - topic_rating_dirobj_description_of(tokens from sentence)")
                print("TODO: parameter tokens: {}".format(sent))
            self.topic_rating_dirobj_description_of(sent)

#Method to debug token atributes.
def debugged_token(token: Token) -> str:
    result = 'Token(%s, lemma=%s' % (token.text, token.lemma_)
    if token._.subject is not None:
        result += ', subject=' + token._.subject.name
    if token._.topic is not None:
        result += ', topic=' + token._.topic.name
    if token._.rating is not None:
        result += ', rating=' + token._.rating.name
    if token._.is_diminisher:
        result += ', diminisher'
    if token._.is_intensifier:
        result += ', intensifier'
    if token._.is_negation:
        result += ', negation'
    result += ')'
    return result
