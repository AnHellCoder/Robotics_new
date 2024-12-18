# Copyright 2021 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import math

from geometry_msgs.msg import TransformStamped

import rclpy
from rclpy.node import Node

from tf2_ros import TransformBroadcaster


class DynamicFrameBroadcaster(Node):

    def __init__(self):
        super().__init__('dynamic_frame_tf2_broadcaster')
        self.tf_broadcaster = TransformBroadcaster(self)
        self.radius = int(self.declare_parameter('radius', '3').get_parameter_value().string_value)
        self.direction_of_rotation = int(self.declare_parameter('direction_of_rotation', '3').get_parameter_value().string_value)
        self.start, _ = self.get_clock().now().seconds_nanoseconds()
        self.timer = self.create_timer(0.1, self.broadcast_timer_callback)

    def broadcast_timer_callback(self):
        #seconds, _ = self.get_clock().now().seconds_nanoseconds()
        #self.get_logger().info(f'{seconds} seconds, {_} _')
        #x = seconds * math.pi

        seconds, nanoseconds = self.get_clock().now().seconds_nanoseconds()
        x = (seconds-self.start+(nanoseconds/10e+8)) * math.pi

        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'turtle1'
        t.child_frame_id = 'carrot1'
        #self.get_logger().info(f'X is {x}, second dif is {seconds-self.start}, nanosecs is {nanoseconds/10e+8}')
        if self.direction_of_rotation == 1:
            t.transform.translation.x = self.radius * math.cos(x) #радиус вращения морковки
            t.transform.translation.y = self.radius * math.sin(x)
        elif self.direction_of_rotation == -1:
            t.transform.translation.x = self.radius * math.sin(x) #радиус вращения морковки
            t.transform.translation.y = self.radius * math.cos(x)
        else:
            raise BaseException("Value must be '1' of '-1'!")
        t.transform.translation.z = 0.0
        t.transform.rotation.x = 0.0
        t.transform.rotation.y = 0.0
        t.transform.rotation.z = 0.0
        t.transform.rotation.w = 1.0

        self.tf_broadcaster.sendTransform(t)


def main():
    rclpy.init()
    node = DynamicFrameBroadcaster()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    rclpy.shutdown()
