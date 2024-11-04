import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node

from action_turtle_interfaces.action import MessageTurtleCommands

from std_msgs.msg import String
from geometry_msgs.msg import Twist

class TurtleActionServer(Node):
    def __init__(self):
        super().__init__('turtle_action_server')
        self._action_server = ActionServer(
            self,
            MessageTurtleCommands,
            'turtle',
            self.execute_callback)
        self.turtle_publisher = self.create_publisher(Twist,
                                 '/turtle1/cmd_vel',
                                 10)

    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal...')
        goal_handle.succeed()

        # print("execute_callback")
        # print(goal_handle.request.command)
        # print(goal_handle.request.s)
        # print(goal_handle.request.angle)

        twist = Twist()

        if goal_handle.request.command == 'forward':
            twist.linear.x = float(goal_handle.request.s)
            twist.angular.z = goal_handle.request.angle*(6/360)
            if goal_handle.request.s > 0:
                self.get_logger().info('Moving forward ' + str(goal_handle.request.s) +
                                        ' cm, and turning ' + str(goal_handle.request.angle) +
                                        ' degrees')
            else:
                self.get_logger().info('Moving backward ' + str(goal_handle.request.s) +
                                        ' cm, and turning ' + str(goal_handle.request.angle) +
                                        ' degrees')

        elif goal_handle.request.command == 'turn_left':
            twist.angular.z = goal_handle.request.angle*(6/360)
            if goal_handle.request.angle == 0:
                self.get_logger().info("I'm not turning")
            else:
                self.get_logger().info('Turning left ' + str(goal_handle.request.angle) + ' degrees')

        elif goal_handle.request.command == 'turn_right':
            twist.angular.z = -goal_handle.request.angle*(6/360)
            if goal_handle.request.angle == 0:
                selt.get_logger().info("I'm not turning")
            else:
                self.get_logger().info('Turning left ' + str(goal_handle.request.angle) + ' degrees')

        self.turtle_publisher.publish(twist)
        
        result = MessageTurtleCommands.Result()
        return result


def main(args=None):
    rclpy.init(args=args)

    turtle_action_server = TurtleActionServer()

    rclpy.spin(turtle_action_server)


if __name__ == '__main__':
    main()