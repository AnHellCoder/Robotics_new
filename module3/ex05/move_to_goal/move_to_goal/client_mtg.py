import sys

from mtg_interfaces.srv import MoveToGoal
import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from geometry_msgs.msg import Twist


class MoveToGoalClient(Node):
    def __init__(self):
        super().__init__('mtg_client')
        self.cli = self.create_client(MoveToGoal, 'move_to_goal')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = MoveToGoal.Request()

    def send_request(self, x, y, theta):
        self.req.x = int(x)
        self.req.y = int(y)
        self.req.theta = int(theta)
        return self.cli.call_async(self.req)


def main():
    rclpy.init()

    mtg_client = MoveToGoalClient()
    future = mtg_client.send_request(str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]))
    rclpy.spin_until_future_complete(mtg_client, future)
    response = future.result()
    mtg_client.get_logger().info(str(response.callback))
    mtg_client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()