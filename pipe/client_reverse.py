from RobotRaconteur.Client import *     #import RR client library
import time, traceback, sys

turtle_change=0


url='rr+tcp://localhost:52222/?service=Create'
#take url from command line
if (len(sys.argv)>=2):
    url=sys.argv[1]

#Startup, connect, and pull out the camera from the objref    
c=RRN.ConnectService(url)


value=1
while True:
	value=np.invert(value)
	c.turtle_change.SendPacket(c.value)   
	time.sleep(1.)
	