#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
import time
import math

rospy.init_node('square_turtle')
publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)

msg=Twist()

while not rospy.is_shutdown():
   start_time=time.time()
   while (time.time() - start_time) < 1:
    msg.linear.x = 1.0
    msg.angular.z = 0.0
    publisher.publish(msg)
    time.sleep(0.1)
    rospy.loginfo("inside first loop")
   
   msg.linear.x = 0.0
   publisher.publish(msg)
   
   start_time=time.time()
   while (time.time() - start_time) < 1:
    msg.linear.x = 0.0
    msg.angular.z = -1*math.pi/2.0
    publisher.publish(msg)
    time.sleep(0.1)
    rospy.loginfo("inside rotation loop")
   msg.angular.z = 0.0
   publisher.publish(msg)
