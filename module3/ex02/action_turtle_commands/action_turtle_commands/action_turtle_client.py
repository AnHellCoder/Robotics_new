import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node

from action_turtle_interfaces.action import MessageTurtleCommands


class TurtleActionClient(Node):
    def __init__(self):
        super().__init__('turtle_action_client')
        self._action_client = ActionClient(self, MessageTurtleCommands, 'turtle')

    def send_goal(self, command, s, angle):
        goal_msg = MessageTurtleCommands.Goal()
        goal_msg.command = command
        goal_msg.s = s
        goal_msg.angle = angle

        print("Goal is going to be sent...")
        print(command, s, angle)

        self._action_client.wait_for_server()

        return self._action_client.send_goal_async(goal_msg)


def main(args=None):
    rclpy.init(args=args)

    action_client = TurtleActionClient()

    future = action_client.send_goal("forward", 5, 90)

    rclpy.spin_until_future_complete(action_client, future)


if __name__ == '__main__':
    main()