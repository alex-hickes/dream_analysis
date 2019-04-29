
from Fralysis.Therapist import Therapist
from Fralysis.InputOutput import InputOutput
from Fralysis.Conversation import Conversation
from Fralysis.Client import Client
from Fralysis.Constants import *
from Fralysis.test.test_data import *
from Fralysis.MessageTypeAnalysis import MessageTypeAnalysis
from Fralysis.Dream import *
from Fralysis.DreamValidator import *


def main(argv=None):
#class StartTherapySession:

	#def __init__(self):
	if DEBUG_ENABLED:
		print("0 - Program starts")

	in_out = InputOutput(interface_type=InputOutput.INTERFACE_TYPE_SIMPLE)
	#in_out = InputOutput(interface_type=InputOutput.INTERFACE_TYPE_KIVY)
	therapist = Therapist(in_out=in_out)

	success = therapist.start_therapy()

	if DEBUG_ENABLED:
		if success:
			print("Therapy was successful")
		else:
			print("Therapy was not successful")


	if DEBUG_ENABLED:
		print("END - Program exits")


if __name__ == "__main__":
    main()


#Concepts:
#-Load up datbase of all saved clients.
#-get the name of a client:
#	If clients name is recognised in database:
#		confirm its correct clients
#		Grab previous information
#	Otherwise create new client and build a dream.
