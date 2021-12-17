from RobotRaconteur.Client import *     #import RR client library
import time, traceback, sys
#RR client setup, connect to turtle service
url='rr+tcp://localhost:12180/?service=fusing_service'


sub=RRN.SubscribeService(url)
obj = sub.GetDefaultClientWait(30)		#connect, timeout=30s


print(obj.current_ply_fabric_type.fabric_name)
print(obj.device_info.model.name)
		