from mtg_interfaces.srv import MoveToGoal
import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

import numpy as np
import time

class MoveToGoalService(Node):
    def __init__(self):
        super().__init__('mtg_service')
        self.srv = self.create_service(MoveToGoal, 'move_to_goal', self.move_to_goal)
        self.turtle_publisher = self.create_publisher(Twist,
                                 '/turtle1/cmd_vel',
                                 10)
        self.pose_listener = self.create_subscription(Pose,
                                                  '/turtle1/pose',
                                                  self.func,
                                                  10)

        self.current_x = None
        self.current_y = None
        self.current_theta = None

    def func(self, msg):
        self.get_logger().info(f'I heard from func {msg.x},{msg.y},{msg.theta}')
        self.current_x = msg.x
        self.current_y = msg.y
        self.current_theta = msg.theta

    def move_to_goal(self, request, response):
        print(f"Your turtle's now on {self.current_x}, {self.current_y}")
        twist = Twist()

        twist.linear.x = float(np.sqrt(np.abs(self.current_x-request.x)**2 + np.abs(self.current_y-request.y)**2))
        twist.angular.z = float(np.arctan(np.abs(self.current_y-request.y)/np.abs(self.current_x-request.x)) + 0.7)
        self.turtle_publisher.publish(twist)

        self.get_logger().info(f'I heard from mtg {request.x},{request.y},{request.theta}')

        return response


def main():
    rclpy.init()

    mtg_service = MoveToGoalService()

    rclpy.spin(mtg_service)

    rclpy.shutdown()


if __name__ == '__main__':
    main()