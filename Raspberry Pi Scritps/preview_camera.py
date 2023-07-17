import paramiko
import sys
import os
import time
import picamera
from scp import SCPClient


framerate=int(sys.argv[1])

#Camera Recording
camera = picamera.PiCamera()
camera.resolution = (640, 600)
camera.framerate=framerate
camera.start_preview()
time.sleep(2)

#Recording control
input("Press ENTER to stop the preview")

