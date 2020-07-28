import RobotRaconteur as RR
RRN=RR.RobotRaconteurNode.s
import time, threading
import numpy as np

minimal_create_interface="""
service experimental.minimal_create

object create_obj
	event turtle_change()
end object
"""

class create_impl(object):
	def __init__(self):   
		self.turtle_change=RR.EventHook()

with RR.ServerNodeSetup("experimental.minimal_create", 52222):
	#Register the service type
	RRN.RegisterServiceType(minimal_create_interface)

	create_inst=create_impl()
	
	#Register the service
	RRN.RegisterService("Create","experimental.minimal_create.create_obj",create_inst)
	
	while True:
		
		create_inst.turtle_change.fire()
		time.sleep(1)
	# input("press enter to quit")
