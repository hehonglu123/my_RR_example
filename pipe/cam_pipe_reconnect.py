# Simple example Robot Raconteur standard camera client
# This program will show a live streamed image from
# the camera.

from RobotRaconteur.Client import *
from RobotRaconteurCompanion.Util.ImageUtil import ImageUtil

import cv2
import sys
import traceback
import argparse
import numpy as np

class CameraClient:
    def __init__(self, url='rr+tcp://localhost:59823?service=camera'):
        self.url = url
        self.current_frame = None
        self.image_util = None
        self.sub = None
        self.cam = None
        self.p = None

        self.failed_connection = False

    def connect_failed(self, s, client_id, url, err):
        # print("Client connect failed: " + str(client_id.NodeID) + " url: " + str(url) + " error: " + str(err))
        self.failed_connection = True

    def new_frame(self, pipe_ep):
        # Loop to get the newest frame
        while pipe_ep.Available > 0:
            # Receive the packet
            image = pipe_ep.ReceivePacket()
            # Convert the packet to an image and set the global variable
            self.current_frame = self.image_util.image_to_array(image)
            return

    def init(self):
        self.sub = RRN.SubscribeService(self.url)
        self.cam = self.sub.GetDefaultClientWait(1)
        self.p = self.sub.SubscribePipe("frame_stream")
        self.sub.ClientConnectFailed += self.connect_failed
        # Create an ImageUtil object to help with image conversion
        self.image_util = ImageUtil(RRN, self.cam)

        # Set the callback for when a new pipe packet is received to the
        # new_frame function
        self.p.PipePacketReceived += self.new_frame

        # Start the camera streaming, ignore error if it is already streaming
        try:
            self.cam.start_streaming()
        except:
            traceback.print_exc()
            pass


    def start(self):
        
        cv2.namedWindow("Image")

        while True:
            if self.failed_connection:
                try:
                    self.cam = self.sub.GetDefaultClientWait(1)
                    self.cam.start_streaming()
                    self.failed_connection = False
                    print("RE-Connected...")
                except:
                    self.failed_connection = True
                    traceback.print_exc()
                    continue
                self.p.PipePacketReceived += self.new_frame
                

            # Display the image
            if self.current_frame is not None:
                cv2.imshow("Image", self.current_frame)
            if cv2.waitKey(50) != -1:
                break
        cv2.destroyAllWindows()

        self.p.Close()
        self.cam.stop_streaming()

if __name__ == '__main__':
    url = 'rr+tcp://localhost:59823?service=camera'
    if len(sys.argv) >= 2:
        url = sys.argv[1]
    client = CameraClient(url)
    client.init()
    client.start()
