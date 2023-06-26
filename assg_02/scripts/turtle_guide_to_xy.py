#!/usr/bin/env python
import rospy
import time
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
import math

msg=Twist()


x_pose=0
y_pose=0
theta=0
k_angular=0.5
k_linear=0.2
goal_reached=False

def pose_callback(data):
    global x_pose,y_pose,theta
    x_pose= data.x
    y_pose= data.y
    theta= data.theta  
 
def error_to_goal(my_pos,goal_pos):
     x_c,y_c,r=my_pos
     x_g,y_g,theta=goal_pos
     x_e,y_e = (x_g-x_c,y_g-y_c)
     error_distance = math.sqrt(x_e*x_e + y_e*y_e)
     b = ((math.atan2(y_e,x_e))+2*(math.pi))%(2*(math.pi))
     error_angle = b - theta
     if abs(error_angle)>math.pi:
        if error_angle > 0:
         error_angle = error_angle - 2*(math.pi)
        else:
         error_angle = error_angle + 2*(math.pi)         
     
     return error_distance, error_angle 
     

def main():
    global goal_reached
    rospy.init_node('turtle_guide_to_xy')
    publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    # Retrieve the parameter value
    target_x = rospy.get_param('/my_param_x')
    target_y = rospy.get_param('/my_param_y')
    r = rospy.get_param('/my_param_r')    
    rospy.Subscriber("/turtle1/pose", Pose, pose_callback)
    
    my_pos = (target_x,target_y,r)
    goal_pos = (x_pose,y_pose,theta)
    
    error_distance,error_angle = error_to_goal(my_pos,goal_pos)
     
    rospy.loginfo("Moving to target:- x:%s; y:%s",target_x,target_y)
    rospy.logdebug("error_distance: %s", error_distance)
    rospy.logdebug("error_angle: %s", error_angle)
    rospy.logdebug("Current position of robot x: %s; y: %s; theta: %s", x_pose, y_pose, theta)
    
    if abs(error_angle)>(math.pi/6) or error_distance>r:
     start_time=time.time()
     msg.linear.x= min(0.3,(k_linear*error_distance))
     while (time.time()-start_time)<1:
      msg.angular.z = -k_angular*error_angle
      publisher.publish(msg)  
    
    else:
      msg.angular.z=0
      msg.linear.x=0
      publisher.publish(msg)
    
    if error_distance<r:
     goal_reached=True
     rospy.loginfo("Goal reached within a radius of %s", r)
    
    
while not rospy.is_shutdown() and not goal_reached:
    main()   
    time.sleep(0.1)
