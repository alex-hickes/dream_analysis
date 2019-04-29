from spacy.tokens import Doc
from Fralysis.Client import Client
from Fralysis.Interview import Interview
from Fralysis.Dream import *
from Fralysis.AnalyseDream import AnalyseDream
from Fralysis.DreamValidator import *
from Fralysis.InputOutput import InputOutput
from Fralysis.Constants import *

#Class Therapist provides chatbot logic and aims to respond to CLient.
#If Client greets Therapist, Therapist should greet back.
#If Client provides their name,Therapist should store this name and proceed.
#If Client provids their dream, Therapist should take neccesary steps to diagnose the dream.
class Therapist:

    def __init__(self, in_out: InputOutput):
        self.in_out = in_out
        self.client = Client()
        self.interview = Interview(client=self.client, in_out=in_out)

    def start_therapy(self):
        if DEBUG_ENABLED:
            print("1 - Therapist ask for name -> Interview")
        if not self.interview.ask_for_name():
            if DEBUG_ENABLED:
                print("2 - ask for name returned None - RETURN False")
            return False

        if DEBUG_ENABLED:
            print("2 - Got Name, ask dream -> Interview")

        if not self.interview.ask_for_dream():
            if DEBUG_ENABLED:
                print("3 - ask for dream returned None - RETURN False")
            return False

        if DEBUG_ENABLED:
            print("3 - Got dream, provide options -> Interview")

        if not self.interview.provide_options():
            if DEBUG_ENABLED:
                print("4 - ask for options returned None. This could be because new dream wasn't recognised or issue with provide_dream() - RETURN False")
            return False

        if DEBUG_ENABLED:
            print("4 - Options provided and further processing complete. provie analysis -> Interview")
        self.interview.give_analysis()

        if DEBUG_ENABLED:
            print("5 - Analysis given - finish_therapy()")
        # return True
        self.finish_therapy()

    def finish_therapy(self):
        if DEBUG_ENABLED:
            print("6 - Therapy Fisnished. Fin.")
        return True
