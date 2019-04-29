from spacy.tokens import Doc
from Fralysis.DreamValidator import *
from Fralysis.InputOutput import InputOutput
from Fralysis.MessageTypeAnalysis import MessageTypeAnalysis
from Fralysis.AnalyseDream import *
from Fralysis.Constants import *
from Fralysis.therapist_conversation_dialogue import *
import random
from statistics import mean

class Conversation:

    def __init__(self, in_out: InputOutput):

        self.in_out = in_out
        self.dream = None

    def get_name(self):
        count = 0
        max_limit = 4

        if DEBUG_ENABLED:
            print("1.1.1 - Write introductory message to user. Enter while count < max_limit")
        self.in_out.write_message(self._random_choice(INTRODUCTION_MESSAGE))

        while count < max_limit:
            count += 1

            if DEBUG_ENABLED:
                print("1.1.2 - Get users message as messageType object")
            message = MessageTypeAnalysis(self.in_out.read_message())

            #TODO: SORT THIS OUT !!!
            if message.is_miscellaneous() == Miscellaneous.GREETING:
                self.in_out.write_message(self._random_choice(GREETING_RESPONSE).format(message.name))
            if message.is_miscellaneous() == Miscellaneous.WEATHER:
                self.in_out.write_message(self._random_choice(WEATHER_RESPONSE))


            if DEBUG_ENABLED:
                print("1.1.3 - If user's message is a name, greet user referencing their name")
            if message.is_name():
                self.in_out.write_message(self._random_choice(FIRST_GREETING).format(message.name))
                if DEBUG_ENABLED:
                    print("1.1.4 - RETURN name")
                return message.is_name()

            if DEBUG_ENABLED:
                print("1.1.4 - Otherwise, repeat requests until count is at max limit. count= {}. Go back to - 1.1.2".format(count))
            if count == 1:
                self.in_out.write_message(self._random_choice(REQUEST_NAME))
            elif count == 2:
                self.in_out.write_message(self._random_choice(REPEAT_REQUEST_NAME))
            else:
                self.in_out.write_message(self._random_choice(URGENT_REQUEST_NAME))


        if DEBUG_ENABLED:
            print("1.1.5 - No name given and max limit reached. Tell user -> RETURN None")
        self.in_out.write_message(self._random_choice(NO_NAME_GIVEN))
        return None

    def get_dream(self, post_opt: PostOption = None):
        count = 0
        min_limit = 2
        max_limit = 10
        validate_dream = None

        if DEBUG_ENABLED:
            print("2.1.1 - Write a request for a dream")
        self.in_out.write_message(self._random_choice(REQUEST_DREAM))

        if DEBUG_ENABLED:
            print("2.1.2 - While count doesn't breach max_limit:")
        while count < max_limit:
            count += 1

            #self.in_out.write_message(self._random_choice(REQUEST_DREAM))
            if DEBUG_ENABLED:
                print("2.1.3 - Get message from user and check if dream:")
            message = MessageTypeAnalysis(self.in_out.read_message())

            if message in NO_MORE_INFO:
                if DEBUG_ENABLED:
                    print("2.1.4 - Message = {}. don't analyse message, but increase count")
                count += 1

            message_nlp = message.is_dream()
            if DEBUG_ENABLED:
                print("2.1.4 - If message is_dream: Check if dream already has a dream. If so, add message to dream messages. If not, create dream with users message")
            # if (message_nlp is not None):
            if (message_nlp):
                # count += 1

                #if (count > 1) or (post_opt is PostOption.MORE_INFO):
                if (self.dream is not None):
                    if DEBUG_ENABLED:
                        print("2.1.5 - Dream exists Add message to existing dream. count should be 2+ count = {}".format(count))
                    self.dream.add_message(message_nlp)
                else:
                    if DEBUG_ENABLED:
                        print("2.1.5 - No dream found. Create new one -> Dream(user msg)")
                    self.dream = Dream(message_nlp)

                AnalyseDream(self.dream)
                validate_dream = DreamValidator(self.dream)

                missing_features = validate_dream.outstanding_features()
                if DEBUG_ENABLED:
                    print("2.1.6 - Analyse and Validate dream. Create list of missing features. missing_features = {}".format(missing_features))
                #TODO: This should really be a sequence of if/else because each time it gets a feature it should go back to the start incase topic and rating given straight after subject request.
                #      But recalling missing feautres seems to work so I'll leave it for now.

                if DEBUG_ENABLED:
                    print("2.1.7 - Check if Subject is missing")

                if Request.SUBJECT in missing_features:
                    self.get_subject()
                    if DEBUG_ENABLED:
                        print("2.1.8 - If count is below min_limit: request more info from user. If message provides more info (doesn't contain: no and is_dream), add message to dream")
                    if count < min_limit:
                        self.in_out.write_message(self._random_choice(MORE_INFO_SUBJECT))
                        #TODO: This may be messing up if user doesn't provie more info and says 'no' instead.
                        more_info_response = self.in_out.read_message()
                        if (MessageTypeAnalysis(more_info_response).is_dream()) and (more_info_response not in NO_MORE_INFO):

                            if DEBUG_ENABLED:
                                print("2.1.9 - more info response from client does provide more info, and message has been added to dream")
                            self.dream.add_message(MessageTypeAnalysis(more_info_response).is_dream())

                if DEBUG_ENABLED:
                    print("2.1.8 - Check if Topic is missing.")

                if Request.TOPIC in missing_features:
                    if DEBUG_ENABLED:
                        print("2.1.9 - Topic is missing - get_topic()")
                    self.get_topic()
                    if DEBUG_ENABLED:
                        print("2.1.11 - If count is below min_limit: request more info from user. If message provides more info (doesn't contian: no and is_dream), add message to dream")
                    if count < min_limit:
                        self.in_out.write_message(self._random_choice(MORE_INFO_TOPIC))
                        #TODO: This may be messing up if user doesn't provie more info and says 'no' instead.
                        more_info_response = self.in_out.read_message()
                        if (MessageTypeAnalysis(more_info_response).is_dream()) and (more_info_response not in NO_MORE_INFO):
                            if DEBUG_ENABLED:
                                print("2.1.12 - More info response from client does provide more info, and message has been added to dream and analysed")
                            self.dream.add_message(MessageTypeAnalysis(more_info_response).is_dream())
                            AnalyseDream(self.dream)

                    if DEBUG_ENABLED:
                        print("2.1.12 - Analyse and Re-validate dream with new messages. Get updated list of missing features")
                        print("TODO: Lets figure out what all our differen't instances of Dream contain.")
                        print("     -self.dream = {}".format(self.dream))
                        #print("     -AnalyseDream(self.dream) = {}".format(AnalyseDream(self.dream)))
                        print("     -validate_dream = {}".format(validate_dream))
                    #AnalyseDream(self.dream)
                    missing_features = validate_dream.outstanding_features()

                if DEBUG_ENABLED:
                    print("2.1.9 - Check if Rating is missing.")

                if Request.RATING in missing_features:
                    if DEBUG_ENABLED:
                        print("2.1.13 - Rating is missing - get_rating()")
                    self.get_rating()
                    if DEBUG_ENABLED:
                        print("2.1.14 - If count is below min_limit: request more info from user. If message provides more info (doesn't contian: no or essential tokens), add message to dream")
                    if count < min_limit:
                        self.in_out.write_message(self._random_choice(MORE_INFO_RATNG))
                        #TODO: This may be messing up if user doesn't provie more info and says 'no' instead.
                        more_info_response = self.in_out.read_message()
                        if (MessageTypeAnalysis(more_info_response).is_dream()) and (more_info_response.lower() not in NO_MORE_INFO):
                            if DEBUG_ENABLED:
                                print("2.1.15 - more info response from client does provide more info, and message has been added to dream")
                            self.dream.add_message(MessageTypeAnalysis(more_info_response).is_dream())
                            AnalyseDream(self.dream)

                    if DEBUG_ENABLED:
                        print("TODO: Should Re-Analyse latest message and validate dream. Shouldn't be looking at previous message features.")
                    validate_dream = DreamValidator(self.dream)

                if validate_dream is not None:
                    if DEBUG_ENABLED:
                        print("2.1.16 - Validate dream. checking to see if updated missing features = {} and count should be greater than {} = {}:".format(validate_dream.outstanding_features(), min_limit, count))
                    if (validate_dream.is_valid()) and (count >= min_limit):
                        if DEBUG_ENABLED:
                            print("2.1.16 - A complete dream has been found (no missing features) and count exceeds min_limit. Dream: {} . count: {} - RETURN complete dream".format(self.dream, count))
                        return self.dream

            if validate_dream is not None:
                if DEBUG_ENABLED:
                    print("2.1.16 - Validate dream. checking to see if updated missing features = {} and count should be greater than {} = {}:".format(validate_dream.outstanding_features(), min_limit, count))
                if (validate_dream.is_valid()) and (count >= min_limit):
                    if DEBUG_ENABLED:
                        print("2.1.16 - A complete dream has been found (no missing features) and count exceeds min_limit. Dream: {} . count: {} - RETURN complete dream".format(self.dream, count))
                    return self.dream

            if DEBUG_ENABLED:
                print("TODO: THIS DOESN@T MAKE SENSE ! ! !")
                if message_nlp is None:
                    print("2.1.5 - Dream is incomplete. This is because message.is_dream() is None. is_dream() = {}. request more dream info depending on count. count = {} go to - 2.1.3 ".format(message.is_dream(), count))
                # else:
                #     if count < min_limit:
                #         #print("2.1.5 - Dream is incomplete because it contains missing features. missing_features = {}. Count = {}. Go to - 2.1.3".format(validate_dream.outstanding_features(), count))
                #     else:
                #         print("2.1.5 - Dream is incomplete because min limit for amount of questions is not reached. Request more dream info depending on count. count = {} go to - 2.1.3".format( count))

            if count == 1:
                self.in_out.write_message(self._random_choice(REQUEST_DREAM))
            elif count == 2:
                self.in_out.write_message(self._random_choice(REPEAT_REQUEST_DREAM))
            else:
                self.in_out.write_message(self._random_choice(URGENT_REQUEST_DREAM))

        if DEBUG_ENABLED:
            print("2.1.18 - max limit exceeded. No dream found - RETURN None")
        self.in_out.write_message(self._random_choice(NO_DREAM_GIVEN))
        return None

    def get_subject(self):
        count = 0
        min_limit = 2
        max_limit = 10

        if DEBUG_ENABLED:
            print("2.2.8.1 - Send message to user requesting Subject")

        self.in_out.write_message(self._random_choice(REQUEST_SUBJECT))

        if DEBUG_ENABLED:
            print("2.2.8.2 - While hasnt exceeded max_limit")
        while count < max_limit:

            if DEBUG_ENABLED:
                print("2.2.8.3 - Read users response. If its a valid dream, add message to dream. Analyse and Validate")
            message = MessageTypeAnalysis(self.in_out.read_message())
            message_nlp = message.is_dream()
            if message_nlp is not None:
                count += 1

                self.dream.add_message(message_nlp)
                AnalyseDream(self.dream)
                validate_dream = DreamValidator(self.dream)

                if DEBUG_ENABLED:
                    print("2.2.8.4 - If Dream no longer has a Subject missing. Return the dreams subject - RETURN dream's subject")
                if Request.SUBJECT not in validate_dream.outstanding_features():
                    if self.dream.get_subject() == Subject.CLIENT:
                        self.in_out.write_message(self._random_choice(CLIENT_SUBJECT_RESPONSE))
                    if self.dream.get_subject() == Subject.SOMEONE:
                        self.in_out.write_message(self._random_choice(SOMEONE_SUBJECT_RESPONSE))
                        #TODO: could be crashing because of topic
                    if self.dream.get_subject() == Subject.OTHER:
                        self.in_out.write_message(self._random_choice(OTHER_SUBJECT_RESPONSE.format(self.dream.get_topics)))
                    return self.dream.get_subject()

            if DEBUG_ENABLED:
                print("2.2.8.5 - Dream still doesn't have a sunject: {} - repeat request for Subject of dream depending on count. count = {} go to 2.2.3".format(self.dream.get_subject(), count))


            if count == 1:
                self.in_out.write_message(self._random_choice(REQUEST_SUBJECT))
            elif count == 2:
                self.in_out.write_message(self._random_choice(REPEAT_REQUEST_SUBJECT))
            else:
                self.in_out.write_message(self._random_choice(URGENT_REQUEST_SUBJECT))

        if DEBUG_ENABLED:
            print("2.2.8.6 - No Subject has been given. Subject = {} - RETURN None".format(self.dream.get_subject()))

        self.in_out.write_message(self._random_choice(NO_SUBJECT_GIVEN))
        return None

    def get_topic(self):
        count = 0
        min_limit = 2
        max_limit = 10

        if DEBUG_ENABLED:
            print("2.2.10.1 - Request topic from user")

        self.in_out.write_message(self._random_choice(REQUEST_TOPIC))

        if DEBUG_ENABLED:
            print("2.2.10.2 - While count doesn't breach max_limit:")
        while count < max_limit:

            if DEBUG_ENABLED:
                print("2.2.10.3 - Read users response. If its a valid dream, add message to dream. Analyse and Validate")
            message = MessageTypeAnalysis(self.in_out.read_message())
            message_nlp = message.is_dream()
            if message_nlp is not None:
                count += 1

                self.dream.add_message(message_nlp)
                AnalyseDream(self.dream)
                validate_dream = DreamValidator(self.dream)

                if DEBUG_ENABLED:
                    print("2.2.10.4 - If Dream no longer has a Topic missing. Return the dreams topic - RETURN dreams topic's")
                if Request.TOPIC not in validate_dream.outstanding_features():
                    self.in_out.write_message(self._random_choice(TOPIC_RESPONSE))
                    return self.dream.get_topics()

            if DEBUG_ENABLED:
                print("2.2.10.5 - Dream still doesn't have a topic: {} - repeat request for Subject of dream depending on count. count = {} go to 2.2.3".format(self.dream.get_topics(), count))

            if count == 1:
                self.in_out.write_message(self._random_choice(REQUEST_TOPIC))
            elif count == 2:
                self.in_out.write_message(self._random_choice(REPEAT_REQUEST_TOPIC))
            else:
                self.in_out.write_message(self._random_choice(URGENT_REQUEST_TOPIC))

        if DEBUG_ENABLED:
            print("2.2.10.6 - No Topic has been given. topics = {} - RETURN None".format(self.dream.get_topics()))
        self.in_out.write_message(self._random_choice(NO_TOPIC_GIVEN))
        return None

    def get_rating(self):
        count = 0
        min_limit = 2
        max_limit = 10

        if DEBUG_ENABLED:
            print("2.2.13.1 - Request rating from user")
        self.in_out.write_message(self._random_choice(REQUEST_RATING))

        if DEBUG_ENABLED:
            print("2.2.13.2 - While count doesn't breach max_limit:")
        while count < max_limit:


            message = MessageTypeAnalysis(self.in_out.read_message())
            if DEBUG_ENABLED:
                print("2.2.13.3 - Read users response. If its a valid dream, add message to dream. message = {}. Analyse and Validate".format(message.message))

            message_nlp = message.is_dream()
            #if message_nlp is not None:
            if message_nlp:
                count += 1

                self.dream.add_message(message_nlp)
                AnalyseDream(self.dream)
                validate_dream = DreamValidator(self.dream)

                if DEBUG_ENABLED:
                    print("2.2.13.4 - If Dream no longer has a Rating missing. Return the dreams Rating - RETURN dreams Rating")
                if Request.RATING not in validate_dream.outstanding_features():
                    self.in_out.write_message(self._random_choice(RATING_RESPONSE))
                    return self.dream.get_ratings()

            if DEBUG_ENABLED:
                print("2.2.10.5 - Dream still doesn't have a Rating: {} - repeat request for Rating of dream depending on count. count = {} go to 2.2.3".format(self.dream.get_ratings(), count))

            if count == 1:
                self.in_out.write_message(self._random_choice(REQUEST_RATING))
            elif count == 2:
                self.in_out.write_message(self._random_choice(REPEAT_REQUEST_RATING))
            else:
                self.in_out.write_message(self._random_choice(URGENT_REQUEST_RATING))


            if DEBUG_ENABLED:
                print("2.2.13.6 - No Rating has been given. Rating = {} - RETURN None".format(self.dream.get_ratings()))
        self.in_out.write_message(self._random_choice(NO_RATING_GIVEN))
        return None

    def get_post_analysis_option(self):

        if DEBUG_ENABLED:
            print("3.1.1 - Send message to user requesting their option: new dream or get analysis")
        self.in_out.write_message(self._random_choice(REQUEST_POST_ANALYSIS_OPTION))

        done = False
        while not done:

            if DEBUG_ENABLED:
                print("3.1.2 - Read users response and check if is_option() -> MessageTypeAnalysis")
            pos_opt = MessageTypeAnalysis(self.in_out.read_message()).is_option()

            if pos_opt == PostOption.NEW_DREAM:
                if DEBUG_ENABLED:
                    print("3.1.3 - User has requested to give another dream - RETURN NEW_DREAM")
                done = True
                return PostOption.NEW_DREAM

            elif pos_opt == PostOption.GET_ANALYSIS:
                if DEBUG_ENABLED:
                    print("3.1.3 - User has requested to get_analysis - RETURN GET_ANALYSIS ")
                done = True
                return PostOption.GET_ANALYSIS

            else:
                if DEBUG_ENABLED:
                    print("3.1.3 - No potion has been provide. Go back to - 3.1.3")
                self.in_out.write_message(self._random_choice(NO_OPTION))

        if DEBUG_ENABLED:
            print("TODO: Do something with the - RETURN")
        return

    # def get_more_info(self):
    #
    #     seeking_more_info = True
    #     if DEBUG_ENABLED:
    #         print("3.1.4.1 - While seeking more information:")
    #     while seeking_more_info:
    #         if DEBUG_ENABLED:
    #             print("3.1.4.2 - Call get_dream(MORE_INFO) - 2.2.1")
    #             print("TODO: This is incomplete. get_dream(MORE_INFO) should recognise more info is being requested")
    #         self.get_dream(PostOption.MORE_INFO)
    #
    #         if DEBUG_ENABLED:
    #             print("3.1.4.3 - Send message to user asking if they have anything more to add")
    #         self.in_out.write_message(self._random_choice(EVEN_MORE_INFO))
    #
    #
    #         if DEBUG_ENABLED:
    #             print("3.1.4.4 - Read message from user and check if contains more info")
    #         provided_info = MessageTypeAnalysis(self.in_out.read_message()).is_dream()
    #         #self.dream.add_message(provided_info)
    #         #AnalyseDream(self.dream)
    #
    #
    #         if (provided_info in MORE_INFO) or (provided_info is not None):
    #             if DEBUG_ENABLED:
    #                 print("3.1.4.5 - User wants to provide more info. Go back to - 3.1.4.2")
    #             continue
    #         else:
    #             if DEBUG_ENABLED:
    #                 print("3.1.4.6 - User doesn't want to provide more info - RETURN provided info")
    #             seeking_more_info = False
    #     return provided_info


    def get_analysis(self, dream: Dream):

        if DEBUG_ENABLED:
            print("4.1.1 - Clients dream is: {}".format(dream))
            print("      -Dream subject: {}".format(dream.get_subject()))
            print("      -Dream direct object: {}".format(dream.get_direct_object()))
            print("      -Dream topics: {}".format(dream.get_topics()))
            print("      -Dream ratings: {}".format(dream.get_ratings()))


        rating = Rating(round((mean([rating.value for rating in dream.get_ratings()])))).name.lower().replace("_"," ")

        if DEBUG_ENABLED:
            print("4.1.2 - Rating is the average of ratings found in the dream. mean of rating: {}".format(rating))
            print("4.1.3 - Topic and Description are converted into readable strings. Context is generated using Subject and rating of dream. Response combines all of this into a single string - RETURN Analysis")


        topic = ', '.join(str(x.name).lower() for x in dream.get_topics()).replace("_"," ")
        desc = ' '.join(x for x in dream.get_descriptions())
        context = ""
        resp = ""

        if dream.get_subject() == Subject.CLIENT:
            context = CREATE_CLIENT_CONTEXT_RESPONSE.format(rating)
        if dream.get_subject() == Subject.SOMEONE:
            context = CREATE_SOMEONE_CONTEXT_RESPONSE.format(rating)
        if dream.get_subject() == Subject.OTHER:
            context =CREATE_OTHER_CONTEXT_RESPONSE.format(rating)

        resp += CREATE_RESPONSE.format(context, topic, desc)
        self.in_out.write_message(resp)
        return resp

    def get_combined_analysis(self, matched_topics: Topic, matched_rating: Rating):

        #Check if there were any similarities:

        resp = ""
        if matched_topics:
            if DEBUG_ENABLED:
                print("4.4.3.1 - Response is initialised to found matched topics")
            resp = "I have found your dreams share topics involving {}.".format(', '.join(str(x.name).lower() for x in matched_topics).replace("_"," "))
        else:
            if DEBUG_ENABLED:
                print("4.4.3.1 - Response is initialised to state no matched topics found")
            resp = "It seems like your dreams do not share any similarities."


        if matched_rating:
            if DEBUG_ENABLED:
                print("4.4.3.2 - Dreams have same rating, write message to user with combined evaluation - RETURN True")
            #resp += "Its seems like your dreams share the same context. They appear {}.".format(', '.join(str(x.name).lower() for x in matched_rating).replace("_"," "))
            resp += "Its seems like your dreams share the same context. They appear {}.".format(matched_rating)
            self.in_out.write_message(resp)
            return True
        #if (not matched_topics) and (not matched_rating):
        else:
            if DEBUG_ENABLED:
                print("4.4.3.2 - Dreams dont have same rating, write message to user with combined evaluation - RETURN True")
            resp += "It seems like your dreams do not share the same context."
            self.in_out.write_message(resp)
            return True

        if DEBUG_ENABLED:
            print("TODO: This shouldnt be seen")
        return False

        #TODO: Create new function which takes multiple dreams.
        #      It will then thry match topics. If match is found.
        #      Make list of matching topics.

    def _random_choice(self, response_list):
            return random.choice(response_list)
