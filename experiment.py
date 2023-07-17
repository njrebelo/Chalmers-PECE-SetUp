import os
import shutil
from imports.InstrumentsInitialization import *

#Experiment Settings
saving_directory="C:\\Users\\PhotonicsUser\\Desktop\\Plots and Data"
saving_directory_vid="C:\\Users\\PhotonicsUser\\Desktop\\Videos"
green_folder="Z:\\Videos ECE-PECE"
os.chdir("C:\\Users\\PhotonicsUser\\Desktop\\ECE")

#Selecting Experiment
fixed_voltage,currlim,data_name,stop=selecting_experiment()

#Start Preview Camera and Check Raspberry Pi status
ssh,name,framerate,tycker=preview_camera(data_name)
 
#Voltage source thing
keithley=voltage_source()
set_currentlim(currlim,keithley)
start_camera(tycker,ssh,name,framerate)
set_voltage(fixed_voltage,keithley)
data_current,data_voltages=measurement(keithley,fixed_voltage,stop)

#Saving data into CSV file
save_labeled(saving_directory,data_current,["Time[s]","Current[mA]"],data_name+"currents",False)
save_labeled(saving_directory,data_voltages,["Time[s]","Voltage[V]"],data_name+"voltages",False)
#Stop camera
end_camera(ssh,name)

#Trnsfer to Green Folder
#try:
#    name=name+".mp4"
#    shutil.copy(saving_directory_vid+"\\"+name, green_folder+"\\"+name)
#    data_name=data_name+".txt"
#    shutil.copy(saving_directory+"\\"+data_name, green_folder+"\\raw_data"+"\\"+data_name)
#except:
#    print("It was not possible to transfer the files to the green folder")
#    time.sleep(10)
    

#Previewing Data
plot_current(data_current,name)
plot_voltage(data_voltages,name)