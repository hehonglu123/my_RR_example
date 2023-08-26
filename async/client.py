from RobotRaconteur.Client import *     #import RR client library
import sys, time

#ASYNC error handler
def my_handler(exp):
	if (exp is not None):
		# If "err" is not None it means that an exception occurred.
		# "err" contains the exception object
		print ("An error occured! " + str(exp))
		return

url='rr+tcp://localhost:52222/?service=Create'
#take url from command line
if (len(sys.argv)>=2):
    url=sys.argv[1]

#Startup, connect, and pull out the camera from the objref    
c=RRN.ConnectService(url)

while True:
	now=time.time()
	c.turtle_x=10.
	print('property change time: ',time.time()-now)
	now=time.time()
	c.async_set_turtle_x(-10., my_handler)	###non-blocking async function
	print('async property change time: ',time.time()-now)
	time.sleep(1)