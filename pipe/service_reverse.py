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

	#pipes
	@property
	def turtle_change(self):
		return self._turtle_change
	@turtle_change.setter
	def turtle_change(self,value):
		self._turtle_change=value
		value.PipeConnectCallback=(self.p1_connect_callback)

	def p1_connect_callback(self,p):
		p.RequestPacketAck=True
		p.PacketReceivedEvent+=self.p1_packet_received

	def p1_packet_received(self,p):
		while p.Available:
			dat=p.ReceivePacket()
			print(dat)
	   


with RR.ServerNodeSetup("experimental.minimal_create", 52222):
	#Register the service type
	RRN.RegisterServiceType(minimal_create_interface)

	create_inst=create_impl()
	
	#Register the service
	RRN.RegisterService("Create","experimental.minimal_create.create_obj",create_inst)
	

	input("press enter to quit")
