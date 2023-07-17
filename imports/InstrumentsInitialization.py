import paramiko
import pyvisa
import os
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import keyboard

"""
With this libary you can initialize all the instrumentation available in the Lab
to use it correctly you always have to import it to your script:
    "from imports.instrumentsInitialization import *" or just replace * with the specific instruments you want to use
The instruments are layed out in the form of functions, with expected inputs and out puts.
When initilizing and instrument you must respect these, for example, lets initialize the ThorLabs PowerMeter:
    
    "thor_labs,intensities,measurments=power_meter(measurments)"
    There will be two expected outputs(you find these in the return of the function), an object call thor_labs, where
    you can control the instrument (you can call it something ele, the import thing is to name it), and an array called
    measurments (again you cna call it something else) which is a data array that you may or not use.
    
    You have only one input called measurments, this should be an integer, which should be the amount of readings per cycle
    of whatever process your script means to do, but again you may not what to use this if your for example just doing
    one read at a time
    
If you run into problems with the initialization of any of the instruments here are some, non-specific, troubleshouting steps:
    1 - Turn off and on the intrument
    2 - Unplug and plug the USB cable
    3 - In the anaconda console, right click one time, select "Quit" and then run your code again.
    4 - Check the error codes in the instrument's screen if one pops up and check it with the manual (you can find it in the folder)
"""
#Pi Information
server="192.168.137.55"
#server="169.254.212.205"
port=22
user="pi"
password="raspberry"

def creatSSHClient(server, port, user, password):
    '''
    This funcion establishes the connection with the rasperrypi

    Parameters
    ----------
    server : String
        IP adress of the raspberry
    port : Int
        Port for communication, 22 as default
    user : String
        pi as default
    password : String
        raspberry as default

    Returns
    -------
    client : Object
        The object to be refrenced
    '''
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, password)
    return client

def preview_camera(data_name):
    '''
    

    Parameters
    ----------
    data_name : TYPE
        DESCRIPTION.

    Returns
    -------
    ssh : TYPE
        DESCRIPTION.
    name : TYPE
        DESCRIPTION.
    framerate : TYPE
        DESCRIPTION.
    tycker : TYPE
        DESCRIPTION.

    '''
    try:
        name=data_name#+time.strftime("%Y%m%d-%H%M%S")
        framerate=int(input("What should be the framerate:"))
        ssh=creatSSHClient(server,port,user,password)
        ssh = ssh.invoke_shell()
        print("Raspberry Pi Initialized")
        ssh.send(f"python ~/Desktop/preview_camera.py {framerate}\n")
        time.sleep(5)
        empty=input("Press ENTER to stop the preview\n")
        ssh.send("\n")
        tycker=1
        return ssh,name,framerate,tycker
    except:
        print("Raspberry Pi Initialization Failed. The process will proceed without the camera.\n If you don't whish to do so, press Ctrl+C")
        tycker=0
        ssh=0
        name=0
        framerate=0
        return ssh,name,framerate,tycker
        
def start_camera(tycker,ssh,name,framerate):
    if tycker==1:
        ssh.send(f"python ~/Desktop/save_camera.py {name} {framerate}\n")
        time.sleep(1)
        return ssh,name,framerate
    else:
        print("")
    
def end_camera(ssh,name):
    empty=input("Press ENTER to stop the recording and save the data\n")
    ssh.send("\n")
    time.sleep(10)
    print("Recording has stopped and been sent\n")
    ssh.close()

def selecting_experiment():
    print("If you are using an PECE set up make sure to turn on the LED current source")
    time.sleep(5)
    fixed_voltage=float(input("What should be the voltage? (in Volts):"))
    time.sleep(1)
    currlim=float(input("What Should be the current limit (in mA):"))
    time.sleep(1)
    stop=float(input("What should be the time resolution between each point?(in seconds, 0 for highest):"))
    data_name=input("What should the data files be named:")
    return fixed_voltage,currlim,data_name,stop

def voltage_source():
    #Initiate Current Source
    rm = pyvisa.ResourceManager()
    #voltage_source=rm.open_resource('GPIB1::5::INSTR')
    voltage_source=rm.open_resource('USB0::0x05E6::0x2280::4444296::0::INSTR')
    print("KEITHLEY INSTRUMENTS,MODEL 2280S-60-3 Initialized\n")
    voltage_source.write("OUTPUT OFF")
    time.sleep(1)
    return voltage_source

def set_voltage(voltage,voltage_source):
    voltage_source.write("VOLT "+str(voltage))
    time.sleep(0.1)
    input("Press ENTER if you wish to proceed\n")
    voltage_source.write("OUTPUT ON")
    time.sleep(0.5)
    volt=voltage_source.query("MEAS:CURR?")
    base=float(volt[15:24])
    exp=float(volt[25:28])
    voltage=base*(pow(10,exp))
    print(f"Voltage at {voltage*1000}mV\n")
    time.sleep(4)
    
def set_currentlim(currlim,voltage_source):
    voltage_source.write("CURR "+str(currlim/1000))
    time.sleep(0.5)
    curr=voltage_source.query("CURR?")
    curr=float(curr[0:6])
    print(f"Current Limit set to {curr*1000}mA\n")
    time.sleep(4)

def measurement(voltage_source,voltage,stop):
    times=[]
    currents=[]
    timesV=[]
    voltages=[]
    start=time.perf_counter()
    print("Press Ctrl-C to stop at any time")
    print("To change the voltage value halfway in the run presse the key V until a coment shows up!\n")
    timesV.append((start-start))
    voltages.append(voltage)
    while True:
        try:
            curr=voltage_source.query("MEAS:CURR?")
            now=time.perf_counter()
            time.sleep(0.5+stop)
            base=float(curr[0:9])
            exp=float(curr[10:13])
            curr=1000*base*(pow(10,exp))
            currents.append(curr)
            times.append((now-start))
            if keyboard.is_pressed("v"):
                time.sleep(2)
                print("What is the new voltage you would like to use:")
                time.sleep(1)
                new_voltage=int(input(""))
                voltage_source.write("VOLT "+str(new_voltage))
                print("New Voltage set\n")
                print("Press Ctrl-C to stop at any time")
                print("To change the voltage value halfway in the run presse the key V until a coment shows up!\n")
                nowV=time.perf_counter()
                timesV.append((nowV-start))
                voltages.append(new_voltage)
                continue
        except ValueError:
            print("You have introduzed a number wrongly, it will be set to the same value as before.")
            print("The etching was not interrupted!\n")
            time.sleep(5)
            print("Press Ctrl-C to stop at any time")
            print("To change the voltage value halfway in the run presse the key V until a coment shows up!\n")
            pass
        except KeyboardInterrupt:
            print("!!You have pressed Ctrl+C the run will be canceled!!\n")
            voltage_source.write("OUTPUT OFF")
            break
    timesV.append((now-start))
    voltages.append(new_voltage)
    data_current=np.vstack((times,currents))
    data_current=np.transpose(data_current)
    data_voltage=np.vstack((timesV,voltages))
    data_voltage=np.transpose(data_voltage)
    return data_current,data_voltage
     
def plot_current(data,name):  
    plt.plot(data[:,0],data[:,1])
    plt.title("Measured Current Over Time ")
    plt.ylabel("Current [mA]")
    plt.xlabel("Time [s]")
    plt.ticklabel_format(useOffset=False)
    plt.savefig("C:\\Users\\PhotonicsUser\\Desktop\\ECE\\data\\"+name+"_current_plot.png")
    plt.show()
    
def plot_voltage(data,name):  
    plt.step(data[:,0],data[:,1],where="post")
    plt.title("Measured Voltage Over Time")
    plt.ylabel("Voltage [V]")
    plt.xlabel("Time [s]")
    plt.ticklabel_format(useOffset=False)
    plt.savefig("C:\\Users\\PhotonicsUser\\Desktop\\ECE\\data\\"+name+"_voltage_plot.png")
    plt.show()
    
def save_labeled(filename,data,labels,text,indexed):
    if not os.path.exists(filename):
        os.makedirs(filename)
    df = pd.DataFrame(data,columns=labels)
    df.to_csv(filename+"\\"+text+".txt",index=indexed)