import math
from math import sin, cos, pi

import json
import serial
import time
import sys
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3


#x = 0.0
#y = 6.4
#th = 0.0

xvalor=0.0
yvalor=0.0
zvalor=0.0

global lineal_prev
global angular_prev
lineal_prev=0.0
angular_prev=0.0

vx = 0.45
vy = -0.1
vth = 0.1
res=False

## --- PRUEBA 1#
ser = serial.Serial(
    port = '/dev/ttyUSB0',
    baudrate = 115200,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS,
    timeout=1.5, 
    inter_byte_timeout=0.1)

ser.close()  
ser.open()   

if ser.isOpen() == True:
	print("Serial communication is open...")
else:
	print("Error opening serial communication")
	#print(dwm_ser.isOpen())



##LO NUEV0
class MinimalPublisher(Node):

    def __init__(self):
    
        super().__init__('hardware_arduino_odom') #NombredelNOdo
        self.publisher_ = self.create_publisher(Odometry, '/odom', 50) 
        timer_period = 0.5  # seconds
        self.i = 0.0
        self.timer_ = self.create_timer(timer_period, self.publish_message)
        
        #Agregado para probar suscripcion
        #super().__init__('py_sub_spiral_node')
        self.subscriber_ = self.create_subscription(Twist, '/cmd_vel', self.subscribe_message, 1)
        self.subscriber_  # prevent unused variable warning

    def publish_message(self):
    
    	if ser.inWaiting()>0:
    	   
           incoming = ser.readline().decode("utf-8")
           incomingDic=json.loads(incoming)
           ##print(ser.inWaiting())		
           ##print(incoming)
           odom=Odometry()
           odom.header.frame_id = "odom"
           # set the position 
           odom.pose.pose.position.x = incomingDic["x"]
           odom.pose.pose.position.y = incomingDic["y"]
           odom.pose.pose.position.z = incomingDic["z"]
           odom.pose.pose.orientation.x = 0.0
           odom.pose.pose.orientation.y = 0.0
           odom.pose.pose.orientation.z = 0.0
           odom.pose.pose.orientation.w = 0.0
           # set the velocity
           odom.child_frame_id = "base_link"
           odom.twist.twist.linear.x = vx
           odom.twist.twist.linear.y = vy
           odom.twist.twist.angular.z = vth
           self.publisher_.publish(odom)
        
           #NUEVO
           ser.flushInput()

    
    def subscribe_message(self, msg):
        global lineal_prev
        global angular_prev
    
        #self.get_logger().info('Recieved - Linear Velocity : %f, Angular Velocity : %f' % (msg.linear.x, msg.angular.z))
        lineal=msg.linear.x
        angular=msg.angular.z
        
        if lineal != lineal_prev or angular != angular_prev:
           #print(lineal)
           #print(lineal_prev)
           data = {}
           data["LW"] =lineal
           data["RW"] =angular
           data=json.dumps(data)
           ser.write(data.encode('ascii'))
           lineal_prev=lineal
           angular_prev=angular
        #ser.flush()
        #time.sleep(0.05)
        
def main(args=None):
    rclpy.init(args=args)
    #minimal_subscriber = MinimalSubscriber()
    minimal_publisher = MinimalPublisher()
    #rclpy.spin(minimal_subscriber)
    rclpy.spin(minimal_publisher)
    #minimal_subscriber.destroy_node()
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
