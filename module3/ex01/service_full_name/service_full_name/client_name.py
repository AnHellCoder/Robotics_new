import sys

from full_name_interfaces.srv import SummFullName
import rclpy
from rclpy.node import Node


class FullNameClient(Node):
    def __init__(self):
        super().__init__('full_name_client')
        self.cli = self.create_client(SummFullName, 'summ_full_name')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = SummFullName.Request()

    def send_request(self, last_name, first_name, patronyme):
        self.req.last_name = last_name
        self.req.first_name = first_name
        self.req.patronyme = patronyme
        return self.cli.call_async(self.req)


def main():
    rclpy.init()

    full_name_client = FullNameClient()
    future = full_name_client.send_request(str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]))
    rclpy.spin_until_future_complete(full_name_client, future)
    response = future.result()
    full_name_client.get_logger().info('Your full name is: ' + response.full_name)
    full_name_clientol.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
