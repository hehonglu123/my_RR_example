from RobotRaconteur.Client import *     #import RR client library
import time, traceback, sys


def my_handler(sub, value, ts):
   # Handle new value
   print(value,ts)

#RR client setup, connect to turtle service
url='rr+tcp://localhost:52222/?service=Create'
#take url from command line
if (len(sys.argv)>=2):
		url=sys.argv[1]

###2 modes available, choose either one		
########wire connection mode:
# obj=RRN.ConnectService(url)
# turtle_change=obj.turtle_change.Connect()


########subscription mode
def connect_failed(s, client_id, url, err):
    print ("Client connect failed: " + str(client_id.NodeID) + " url: " + str(url) + " error: " + str(err))

sub=RRN.SubscribeService(url)
obj = sub.GetDefaultClientWait(30)		#connect, timeout=30s
turtle_change_sub=sub.SubscribeWire("turtle_change")


sub.ClientConnectFailed += connect_failed

turtle_change_sub.WireValueChanged += my_handler
input('press enter to quit')