import RobotRaconteur as RR
RRN=RR.RobotRaconteurNode.s
import time, threading
import numpy as np
from RobotRaconteur.RobotRaconteurPythonError import StopIterationException

minimal_create_interface="""
service experimental.minimal_create

object create_obj
	function double{generator} iterate(int32 a, int32 b)
end object
"""

class create_impl(object):
	def __init__(self):   
		self._turtlechange=None
		self.value=1

	def iterate(self,a,b):
		for i in range(a,b):
			yield i
			if i==b-1:
				raise StopIterationException("Procedure completed")
				return

with RR.ServerNodeSetup("experimental.minimal_create", 52222):
	#Register the service type
	RRN.RegisterServiceType(minimal_create_interface)

	create_inst=create_impl()
	
	#Register the service
	RRN.RegisterService("Create","experimental.minimal_create.create_obj",create_inst)
	
	input('press enter to quit')