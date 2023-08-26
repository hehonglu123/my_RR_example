import RobotRaconteur as RR
RRN=RR.RobotRaconteurNode.s
import time
import numpy as np
import copy

minimal_create_interface="""
service experimental.minimal_create

object create_obj
	property double turtle_x
end object
"""

class create_impl(object):
	def __init__(self):   
		self.turtle_x=0


with RR.ServerNodeSetup("experimental.minimal_create", 52222):
	#Register the service type
	RRN.RegisterServiceType(minimal_create_interface)

	create_inst=create_impl()
	
	#Register the service
	RRN.RegisterService("Create","experimental.minimal_create.create_obj",create_inst)
	
	input('press enter to quit')
