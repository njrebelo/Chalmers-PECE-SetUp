import sys
import paramiko
import os
import time
import picamera
from scp import SCPClient

#SCP Info, for the PC
server="169.254.179.25"
port=22
user="nelso"
password="triviaLock101"

#Savind settings Pi
experiment_directory="/home/pi/Desktop/Electrochemical_Videos"
specified_name=input(sys.argv[1]) #The specific name you want to give
current_time=time.strftime("%Y%m%d-%H%M%S")
videoname=specified_name+"_"+current_time+".h264"

#Export Location
directory_pc="C://Users//nelso//OneDrive//Documentos//Videos"
duration=int(sys.argv[2])
framerate=int(sys.argv[3])

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
camera.wait_recording(duration)
camera.stop_recording()

#Send File
scp.put(experiment_directory+"//"+videoname, recursive=True, remote_path=directory_pc)
