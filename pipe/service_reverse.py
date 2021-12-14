import RobotRaconteur as RR
RRN=RR.RobotRaconteurNode.s
import time, threading
import numpy as np

minimal_create_interface="""
service experimental.minimal_create

object create_obj
	pipe int8 turtle_change [writeonly]
end object
"""

class create_impl(object):
	def __init__(self):   
		self._turtlechange=None
		self.value=1

	def update(self):
		self.value=np.invert(self.value)
		self.turtle_change.SendPacket(self.value)

	def new_frame(pipe_ep):
	    print(self.turtle_change)
	    #Loop to get the newest frame
	    while (pipe_ep.Available > 0):
	        #Receive the packet
	        self.turtle_change=pipe_ep.ReceivePacket()


with RR.ServerNodeSetup("experimental.minimal_create", 52222):
	#Register the service type
	RRN.RegisterServiceType(minimal_create_interface)

	create_inst=create_impl()
	
	#Register the service
	RRN.RegisterService("Create","experimental.minimal_create.create_obj",create_inst)
	
	#Connect the pipe FrameStream to get the PipeEndpoint p
	p=create_inst.turtle_change.Connect(-1)

	#Set the callback for when a new pipe packet is received to the
	#new_frame function
	p.PacketReceivedEvent+=create_inst.new_frame

	input("press enter to quit")
