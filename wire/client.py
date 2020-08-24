from RobotRaconteur.Client import *     #import RR client library
import time, traceback, sys
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
while True:
	try:
		obj = sub.GetDefaultClient()
		turtle_change=sub.SubscribeWire("turtle_change")
		break
	except RR.ConnectionException:
		time.sleep(0.1)

sub.ClientConnectFailed += connect_failed

while True:
	time.sleep(0.1)
	if turtle_change.TryGetInValue()[0]:
		print(turtle_change.InValue)
		