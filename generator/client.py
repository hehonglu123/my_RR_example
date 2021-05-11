from RobotRaconteur.Client import *     #import RR client library
import time, traceback, sys


url='rr+tcp://localhost:52222/?service=Create'
#take url from command line
if (len(sys.argv)>=2):
    url=sys.argv[1]

#Startup, connect, and pull out the camera from the objref    
c=RRN.ConnectService(url)

#Connect the pipe FrameStream to get the PipeEndpoint p
temp=c.iterate(1,10)
start_val=temp.next()

while (True):
    try:
        start_val=temp.next()
        print(start_val)
    except RR.StopIterationException:
        break