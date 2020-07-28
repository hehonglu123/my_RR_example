from RobotRaconteur.Client import *     #import RR client library
import time, traceback, sys

turtle_change=0
def new_frame(pipe_ep):
    global turtle_change
    print(turtle_change)
    #Loop to get the newest frame
    while (pipe_ep.Available > 0):
        #Receive the packet
        turtle_change=pipe_ep.ReceivePacket()




url='rr+tcp://localhost:52222/?service=Create'
#take url from command line
if (len(sys.argv)>=2):
    url=sys.argv[1]

#Startup, connect, and pull out the camera from the objref    
c=RRN.ConnectService(url)

#Connect the pipe FrameStream to get the PipeEndpoint p
p=c.turtle_change.Connect(-1)

#Set the callback for when a new pipe packet is received to the
#new_frame function
p.PacketReceivedEvent+=new_frame

input("press enter to quit")
	