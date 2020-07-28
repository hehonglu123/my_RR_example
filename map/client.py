from RobotRaconteur.Client import *     #import RR client library
import sys, time

url='rr+tcp://localhost:52222/?service=Create'
#take url from command line
if (len(sys.argv)>=2):
    url=sys.argv[1]

#Startup, connect, and pull out the camera from the objref    
c=RRN.ConnectService(url)

i=0
while True:
	print(c.turtle_dict['turtle'+str(i)].turtle_pose.x)
	i+=1
	time.sleep(1)