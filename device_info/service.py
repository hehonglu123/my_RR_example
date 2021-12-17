#!/usr/bin/python3
import RobotRaconteur as RR
RRN=RR.RobotRaconteurNode.s
import RobotRaconteurCompanion as RRC
from RobotRaconteurCompanion.Util.InfoFileLoader import InfoFileLoader
from RobotRaconteurCompanion.Util.DateTimeUtil import DateTimeUtil
from RobotRaconteurCompanion.Util.AttributesUtil import AttributesUtil
from RobotRaconteur.RobotRaconteurPythonError import StopIterationException
import sys, os, time, argparse, traceback, cv2, copy, yaml
import numpy as np



class fusing_pi(object):
	def __init__(self,device_info):
		self._device_info=device_info
		self.current_ply_fabric_type=RRN.NewStructure("edu.rpi.robotics.fusing_system.FabricInfo")
		self.current_interlining_fabric_type=RRN.NewStructure("edu.rpi.robotics.fusing_system.FabricInfo")
		self.error_message_type=RRN.NewStructure("com.robotraconteur.eventlog.EventLogMessage")
		self.current_errors=[]

		self.current_ply_fabric_type.fabric_name='PD19_016C-FR-LFT-LWR HICKEY 36'
		self.current_interlining_fabric_type.fabric_name='PD19_016C-FR-LFT-LWR-INT HICKEY 36'

	@property
	def device_info(self):
		return self._device_info


def main():
	RRC.RegisterStdRobDefServiceTypes(RRN)

	with open('test.yml') as file:
		robot_info_text = file.read()

	info_loader = InfoFileLoader(RRN)
	robot_info, robot_ident_fd = info_loader.LoadInfoFileFromString(robot_info_text, "com.robotraconteur.robotics.robot.RobotInfo", "robot")

	attributes_util = AttributesUtil(RRN)
	robot_attributes = attributes_util.GetDefaultServiceAttributesFromDeviceInfo(robot_info.device_info)

	with RR.ServerNodeSetup("fusing_service",12180) as node_setup:
		
		RRN.RegisterServiceTypeFromFile("edu.rpi.robotics.fusing_system")

		fusing_pi_obj=fusing_pi(robot_info.device_info)
	
		service_ctx = RRN.RegisterService("fusing_service","edu.rpi.robotics.fusing_system.FusingSystem",fusing_pi_obj)


		input('press enter to quit')


if __name__ == '__main__':
	main()
