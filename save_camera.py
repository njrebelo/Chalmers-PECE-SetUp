import paramiko
import sys
import os
import time
import picamera
from scp import SCPClient

#SCP Info, for the PC
server="129.16.139.105"
port=22
user="PhotonicsUser"
password="User_Photonics"

#Savind settings Pi
experiment_directory="/home/pi/Desktop/Electrochemical_Videos"
videoname=sys.argv[1]+".h264" #It can also be MJPEG

#Export Location
directory_pc="C:/Users/PhotonicsUser/Desktop/ECE/Videos"
framerate=int(sys.argv[2])

def createSSHClient(server, port, user, password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, password)
    return client

#PC Connection
ssh = createSSHClient(server, port, user, password)
scp = SCPClient(ssh.get_transport())

#Camera Recording
camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.framerate=framerate
camera.start_preview()
time.sleep(2)
camera.start_recording(experiment_directory+"//"+videoname)
start=time.perf_counter()

#Recording control
input("Press ENTER to Stop the recording")
camera.stop_recording()

#Send File
scp.put(experiment_directory+"//"+videoname, recursive=True, remote_path=directory_pc)
