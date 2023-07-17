import os
import sys
import time
import picamera

#Savind settings Pi
experiment_directory="/home/pi/Desktop/Electrochemical_Videos"
specified_name=sys.argv[1] #The specific name you want to give
videoname=specified_name+".h264" #It can also be MJPEG

#Export Location
directory_pc="C://Users//user//Documentos//Videos"
framerate=int(sys.argv[2])

#Camera Recording
camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.framerate=framerate
camera.start_preview()
time.sleep(2)
camera.start_recording(experiment_directory+"//"+videoname)
time.sleep(10000)
