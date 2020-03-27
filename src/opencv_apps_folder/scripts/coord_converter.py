
# CALCULATING WORLD COORDINATES FROM IMAGE COORDINATES
#
#
# P_image = I * P_world 
#
#
# | x_image | = I * | x_world |
# | y_image |       | y_world |
# |    1    |       | z_world |
#                   |    1    |
# Where
#
# I = | f_x    0    c_x    0 | 
#     |  0    f_y   c_y    0 |
#     |  0     0     1     0 |
#
# So
#
#############################################
# x_world = (x_image - c_x) * z_world / f_x #
# y_world = (y_image - c_y) * z_world / f_y #
#############################################
#
# We can get c_x, c_y, f_x, f_y using PinholeCameraModel from image_geometry
#
#
#!/usr/bin/env python
import roslib
import sys
import rospy
import cv2
import numpy as np
from opencv_apps.msg import CircleArrayStamped
from sensor_msgs.msg import CameraInfo
from cv_bridge import CvBridge, CvBridgeError
from distutils.version import LooseVersion
from image_geometry import PinholeCameraModel

class coord_converter:

  def __init__(self):
    self.image_sub = rospy.Subscriber("hough_circles/circles", CircleArrayStamped, self.callback)
    self.camera_info_msg = None
    self.camera_model = PinholeCameraModel() 
    self.image_info_sub = rospy.Subscriber("camera1/camera_info", CameraInfo, self.image_info_cb, queue_size=1) 

#    if self.camera_info_msg is not None:
#	print('PinholeCameraModel parameters:\n')
#       print('cx: ' + str(self.camera_model.cx()))
#	print('cy: ' + str(self.camera_model.cy()))
#	print('fx: ' + str(self.camera_model.fx()))
#	print('fy: ' + str(self.camera_model.fy()))

  def callback(self,data):
    print('\nIMAGE COORDINATES (center):')
    for i in range (len(data.circles)):
      print(' circle' + str(i+1) + ' detected:')
      print('  x: ' + str(data.circles[i].center.x))
      print('  y: ' + str(data.circles[i].center.y))
      
    print('\nWORLD COORDINATES (center):')
    print(' camera_robot coordinates:\n  x: 1.4\n  y: 2.2')
    for i in range (len(data.circles)):
      print(' circle' + str(i+1) + ' detected:')
      # using the equations showed at the beggining of this script:
      x_world = ((data.circles[i].center.x) - self.camera_model.cx()) * 1.25 / self.camera_model.fx() #z_world = camera rod height = 1.25
      y_world = ((data.circles[i].center.y) - self.camera_model.cy()) * 1.25 / self.camera_model.fy()
      print('  x: ' + str(1.4 + x_world)) #x=0 from image = 1.4 from world
      print('  y: ' + str(2.6 - y_world)) #y=0 from image = 2.6 from world / direction of y axis from world = -y from image

  def image_info_cb(self, msg):
    if self.camera_info_msg is None:
      self.camera_model.fromCameraInfo(msg)
      self.camera_info_msg = msg
  
def main():
  cc = coord_converter()
  rospy.init_node('coord_converter', anonymous=True)

  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")

if __name__ == '__main__':
    main()
