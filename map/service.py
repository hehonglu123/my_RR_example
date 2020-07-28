import RobotRaconteur as RR
RRN=RR.RobotRaconteurNode.s
import time
import numpy as np
import copy

minimal_create_interface="""
service experimental.minimal_create
struct pose
    field double x
    field double y
    field double angle
end
struct turtle
	field string name
	field int8 index
	field pose turtle_pose
	field string color
end
object create_obj
	property turtle{string} turtle_dict
end object
"""

class create_impl(object):
	def __init__(self):   
		self.turtle=RRN.NewStructure("experimental.minimal_create.turtle")
		self.turtle.turtle_pose=RRN.NewStructure("experimental.minimal_create.pose")
		self.turtle_dict={}
		self.turtle_dict['turtle0']=self.turtle


with RR.ServerNodeSetup("experimental.minimal_create", 52222):
	#Register the service type
	RRN.RegisterServiceType(minimal_create_interface)

	create_inst=create_impl()
	
	#Register the service
	RRN.RegisterService("Create","experimental.minimal_create.create_obj",create_inst)
	
	i=0
	while True:
		i+=1
		create_inst.turtle_dict['turtle'+str(i)]=copy.deepcopy(create_inst.turtle)
		create_inst.turtle_dict['turtle'+str(i)].turtle_pose.x=i
		time.sleep(1)
