import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge
import cv2
import numpy as np

class BlueDetector(Node):
    def __init__(self):
        super().__init__('blue_detector')
        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10)
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.bridge = CvBridge()

    def image_callback(self, msg):
        # Convert ROS Image message to OpenCV image
        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

        # Convert the image from BGR to HSV
        hsv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)

        # Define the range for blue color in HSV
        lower_blue = np.array([100, 150, 0])
        upper_blue = np.array([140, 255, 255])

        # Create a mask for blue color
        mask = cv2.inRange(hsv_image, lower_blue, upper_blue)

        # Check if any blue color is detected
        if np.any(mask):
            self.get_logger().info('Blue color detected, stopping the robot.')
            self.stop_robot()
        else:
            self.get_logger().info('No blue color detected.')

    def stop_robot(self):
        # Publish zero velocity to stop the robot
        twist = Twist()
        twist.linear.x = 0.0
        twist.angular.z = 0.0
        self.publisher_.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    blue_detector = BlueDetector()
    rclpy.spin(blue_detector)
    blue_detector.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()