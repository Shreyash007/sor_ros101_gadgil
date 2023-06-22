#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64
from assg_01.msg import Cylinder
from assg_01.msg import Cylinder_weight


from math import pi

volume=0
density=0

volume_found=False
density_found=False

def volume_callback(data):
  global volume
  global volume_found
  volume=data.volume
  volume_found=True
  
def density_callback(data):
  global density
  global density_found
  density=data.data
  density_found=True

def calculate():
  if volume_found and density_found:
  	msg=Cylinder_weight()  	
  	msg.weight = density*volume 
  	pub.publish(msg)

rospy.init_node("cylinder_weight")
rospy.Subscriber("/cylinder", Cylinder, volume_callback)
rospy.Subscriber("/density", Float64, density_callback)
pub=rospy.Publisher("/cylinder_weight",Cylinder_weight, queue_size=10)

while not rospy.is_shutdown():
	calculate()
	rospy.sleep(0.1)
	
	
