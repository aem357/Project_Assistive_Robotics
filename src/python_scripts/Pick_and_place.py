import os
import time
from math import radians, degrees, pi
from robodk.robolink import Robolink
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

def Init():
    print("Init")
    robot.MoveL(Init_target, True)
    print("Init_target REACHED")

def Pick():
    print("Pick") 

    # Mover el robot para acercarse al objetivo
    robot.MoveL(App_pick_target, True)  

    robot.setSpeed(20)  # Reducir la velocidad del robot
    robot.MoveL(Pick_target, True)  # Mover el robot al objetivo de recogida
    
    cube.setParentStatic(tool)  # Pegar el cubo a la pinza
    robot.MoveL(App_pick_target, True)  # Mover el robot de vuelta al target
    
    print("Pick FINISHED")

def Place():
 
    print("Place")

     # Aumentar de vuelta la velocidad del robot
    robot.setSpeed(60)
    robot.MoveL(App_place_target, True)  # Mover el robot al target 

    # # Reducir la velocidad del robot
    robot.setSpeed(20)
    robot.MoveL(Place_target, True)  # Mover el robot al target

    # Soltar el cubo en la mesa
    cube.setParentStatic(table)

    # Mover el robot de regreso al target
    robot.MoveL(App_place_target, True)

    print("Place FINISHED")

# Main function
def main():
    Init()
    Pick()
    Place()

if __name__ == "__main__":
    main()
