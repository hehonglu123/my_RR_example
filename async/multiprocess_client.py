from multiprocessing import Process
from RobotRaconteur.Client import *     #import RR client library
import sys, time

def my_function(x):
	print('Function started: ',x)
	time.sleep(2)  # Simulate a long-running operation
	x+=10
	print('Function finished: ',x)
	return 

def main():
	url='rr+tcp://localhost:52222/?service=Create'
	#take url from command line
	if (len(sys.argv)>=2):
		url=sys.argv[1]

	#Startup, connect, and pull out the camera from the objref    
	c=RRN.ConnectService(url)

	while True:
		now=time.time()
		process = Process(target=my_function,args=(c.turtle_x,))
		process.start()
		c.turtle_x=10.
		print('property change time: ',time.time()-now)
		time.sleep(2)
if __name__ == '__main__':	###GUARANTEED SAFE IMPORT, necessary for Multiprocessing
    main()