import paramiko
import os
import sys
import time
import picamera
from scp import SCPClient

#SCP Info, for the PC
server="169.254.69.114"
port=22
user="user"
password="mc2mc2"

#Savind settings Pi
experiment_directory="/home/pi/Desktop/Electrochemical_Videos"
specified_name=arg.sys[1] #The specific name you want to give
videoname=specified_name+".h264" #It can also be MJPEG

#Export Location
directory_pc="C://Users//user//Documentos//Videos"

def createSSHClient(server, port, user, password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, password)
    return client

#PC Connection
ssh = createSSHClient(server, port, user, password)
scp = SCPClient(ssh.get_transport())

camera.stop_recording()

#Send File
scp.put(experiment_directory+"//"+videoname, recursive=True, remote_path=directory_pc)
