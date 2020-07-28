import RobotRaconteur as RR
RRN=RR.RobotRaconteurNode.s
import time, threading
import numpy as np

minimal_create_interface="""
service experimental.minimal_create

object create_obj
	pipe int8 turtle_change [readonly]
end object
"""

class create_impl(object):
	def __init__(self):   
		self._turtlechange=None

		self.value=1

	#turtle_change pipe member property getter and setter
	@property
	def turtle_change(self):
		return self._turtlechange
	@turtle_change.setter
	def turtle_change(self,value):
		self._turtlechange=value
		#Create the PipeBroadcaster and set backlog to 3 so packets
		#will be dropped if the transport is overloaded
		self._turtlechange_broadcaster=RR.PipeBroadcaster(value,1)

	def update(self):
		self.value=np.invert(self.value)
		self._turtlechange_broadcaster.AsyncSendPacket(self.value,lambda: None)   

with RR.ServerNodeSetup("experimental.minimal_create", 52222):
	#Register the service type
	RRN.RegisterServiceType(minimal_create_interface)

	create_inst=create_impl()
	
	#Register the service
	RRN.RegisterService("Create","experimental.minimal_create.create_obj",create_inst)
	
	while True:
		
		create_inst.update()
		time.sleep(1)
