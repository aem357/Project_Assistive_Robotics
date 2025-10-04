import time
from math import radians, degrees, pi
from robodk.robolink import Robolink
from robodk.robomath import *

# Robot setup
RDK = Robolink()
robot = RDK.Item("UR5e")
base = RDK.Item("UR5e Base")
tool = RDK.Item('2FG7')
Init_target = RDK.Item('Init')
App_pick_target = RDK.Item('App_Pick')
Pick_target = RDK.Item('Pick')
App_place_target = RDK.Item('App_Place')
Place_target = RDK.Item('Place')
table = RDK.Item("Table")
cube = RDK.Item('cube')
cube.setVisible(False)
cube_POSE=Pick_target.Pose()
cube.setParent(table)# Do not maintain the actual absolute POSE
cube.setPose(cube_POSE)
cube.setVisible(True)

robot.setPoseFrame(base)
robot.setPoseTool(tool)
robot.setSpeed(20)

def Init():
    print("Init")
    robot.MoveL(Init_target, True)
    print("Init_target REACHED")

def Pick():
    print("Pick")
    
    # Move to the approach pick target
    robot.MoveL(App_pick_target, True)
    print("Approach Pick Target REACHED")
    
    # Move to the pick target
    robot.MoveL(Pick_target, True)
    print("Pick Target REACHED")
    
    # Attach the cube to the tool
    cube.setParentStatic(tool)  # Maintain the actual absolute POSE
    print("Cube ATTACHED to the tool")
    
    # Move back to the approach pick target
    robot.MoveL(App_pick_target, True)
    print("Pick FINISHED")

def Place():
    print("Place")
    
    # Move to the approach place target
    robot.MoveL(App_place_target, True)
    print("Approach Place Target REACHED")
    
    # Move to the place target
    robot.MoveL(Place_target, True)
    print("Place Target REACHED")
    
    # Detach the cube from the tool
    cube.setParent(table)  # Reparent the cube to the table
    print("Cube DETACHED from the tool")
    
    # Move back to the approach place target
    robot.MoveL(App_place_target, True)
    print("Place FINISHED")

# Main function
def main():
    Init()
    Pick()
    Place()
