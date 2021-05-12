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
class iter_gen(object):
	def __init__(self,a,b):
		self.a=a
		self.b=b
		self.value=a
		self._aborted=False

	def Next(self):
		if self._aborted:
			raise OperationAbortedException()
		
		if self.value>=self.b:
			raise StopIterationException()
		
		self.value+=1
		return self.value
		
	def Abort(self):
		self._aborted=True
		
	def Close(self):
		raise StopIterationException()


class create_impl(object):
	def __init__(self):   
		self.value=1

	def iterate(self,a,b):
		return iter_gen(a,b)

with RR.ServerNodeSetup("experimental.minimal_create", 52222):
	#Register the service type
	RRN.RegisterServiceType(minimal_create_interface)

	create_inst=create_impl()
	
	#Register the service
	RRN.RegisterService("Create","experimental.minimal_create.create_obj",create_inst)
	
	input('press enter to quit')