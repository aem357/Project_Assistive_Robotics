import os
import time
import socket
from math import radians, degrees, pi
import numpy as np
from robodk.robolink import *
from robodk.robomath import *

# Define relative path to .rdk file
relative_path = "src/roboDK/Pick&Place_UR5e.rdk"
absolute_path = os.path.abspath(relative_path)

# Start RoboDK with the project file
RDK = Robolink()
RDK.AddFile(absolute_path)

# Robot setup
robot = RDK.Item("UR5e")
base = RDK.Item("UR5e Base")
tool = RDK.Item("2FG7")
Init_target = RDK.Item("Init")
App_pick_target = RDK.Item("App_Pick")
Pick_target = RDK.Item("Pick")
App_place_target = RDK.Item("App_Place")
Place_target = RDK.Item("Place")
table = RDK.Item("Table")
cube = RDK.Item("Cube")

cube.setVisible(False)
cube_POSE = Pick_target.Pose()
cube.setParent(table)  # Do not maintain the actual absolute POSE
cube.setPose(cube_POSE)
cube.setVisible(True)

robot.setPoseFrame(base)
robot.setPoseTool(tool)
robot.setSpeed(70)

# Robot Constants
ROBOT_IP = '192.168.1.4'
ROBOT_PORT = 30002
accel_mss = 1.2
speed_ms = 0.75
time_high = 5
blend_r = 0.0
timej = 6
timel = 4

# URScript commands
set_tcp = "set_tcp(p[0.000000, 0.000000, 0.1470000, 0.000000, 0.000000, 0.000000])"
j1, j2, j3, j4, j5, j6 = np.radians(Init_target.Joints()).tolist()[0]
movel_Init_target = f"movel([{j1},{j2}, {j3}, {j4}, {j5}, {j6}],{accel_mss},{speed_ms},{time_high},{blend_r})"
j1, j2, j3, j4, j5, j6 = np.radians(App_pick_target.Joints()).tolist()[0]
movel_App_pick_target = f"movel([{j1},{j2}, {j3}, {j4}, {j5}, {j6}],{accel_mss},{speed_ms},{time_high},{blend_r})"
j1, j2, j3, j4, j5, j6 = np.radians(Pick_target.Joints()).tolist()[0]
movel_Pick_target = f"movel([{j1},{j2}, {j3}, {j4}, {j5}, {j6}],{accel_mss},{speed_ms},{time_high},{blend_r})"
j1, j2, j3, j4, j5, j6 = np.radians(App_place_target.Joints()).tolist()[0]
movel_App_place_target = f"movel([{j1},{j2}, {j3}, {j4}, {j5}, {j6}],{accel_mss},{speed_ms},{time_high},{blend_r})"
j1, j2, j3, j4, j5, j6 = np.radians(Place_target.Joints()).tolist()[0]
movel_Place_target = f"movel([{j1},{j2}, {j3}, {j4}, {j5}, {j6}],{accel_mss},{speed_ms},{time_high},{blend_r})"

# Check robot connection
def check_robot_port(ip, port):
    global robot_socket
    try:
        robot_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        robot_socket.settimeout(1)
        robot_socket.connect((ip, port))
        return True
    except (socket.timeout, ConnectionRefusedError):
        return False
    
# Send URScript command
def send_ur_script(command):
    robot_socket.send((command + "\n").encode())

def receive_response(t):
    try:
        print("Waiting time:", t)
        time.sleep(t)
    except socket.error as e:
        print(f"Error receiving data: {e}")
        exit(1)

def Init():
    print("Init")
    robot.MoveL(Init_target, True) #Cambiarlo con IF para mover con ur5e_execution y robot_is_connected y mandar el socket
    print("Init_target REACHED")
    if robot_is_connected and ur5e_execution:
        print("Init REAL UR5e")
        send_ur_script(set_tcp)
        receive_response(1)
        send_ur_script(movel_Init_target)
        receive_response(timej)
    else:
        print("UR5e not connected. Simulation only.")

def Pick():
    print("Pick") 

    # Mover el robot para acercarse al objetivo
    robot.MoveL(App_pick_target, True)  

    robot.setSpeed(20)  # Reducir la velocidad del robot
    robot.MoveL(Pick_target, True)  # Mover el robot al objetivo de recogida
    
    cube.setParentStatic(tool)  # Pegar el cubo a la pinza
    robot.MoveL(App_pick_target, True)  # Mover el robot de vuelta al target

    print("Pick FINISHED")
    if robot_is_connected and ur5e_execution:
        print("Pick REAL UR5e")
        send_ur_script(set_tcp)
        receive_response(1)
        send_ur_script(movel_App_pick_target)
        receive_response(timel)
        send_ur_script(movel_Pick_target)
        receive_response(timel)
        send_ur_script(movel_App_pick_target)
        receive_response(timel)

def Place():

    print("Place")

    # Aumentar de vuelta la velocidad del robot
    robot.setSpeed(60)
    robot.MoveL(App_place_target, True)  # Mover el robot al target 

    # Reducir la velocidad del robot
    robot.setSpeed(20)
    robot.MoveL(Place_target, True)  # Mover el robot al target

    # Soltar el cubo en la mesa
    cube.setParentStatic(table)

    # Mover el robot de regreso al target
    robot.MoveL(App_place_target, True)

    print("Place FINISHED")

# Main function
def main():
    global robot_is_connected, ur5e_execution
    ur5e_execution = True # Flag for UR5e execution. Only one group at True at a time.
    robot_is_connected = check_robot_port(ROBOT_IP, ROBOT_PORT)
    Init()
    Pick()
    Place()
    if robot_is_connected:
        robot_socket.close()

if __name__ == "__main__":
    main()
    #METODO 2
