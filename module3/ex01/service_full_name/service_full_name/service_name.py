from full_name_interfaces.srv import SummFullName

import rclpy
from rclpy.node import Node


class FullNameService(Node):
    def __init__(self):
        super().__init__('full_name_service')
        self.srv = self.create_service(SummFullName, 'summ_full_name', self.concat_names_callback)

    def concat_names_callback(self, request, response):
        response.full_name = request.last_name + ' ' + request.first_name + ' ' + request.patronyme
        self.get_logger().info('Incoming request\nlast name: ' + str(request.last_name) + ', first name: ' + str(request.first_name) + ', patronyme: ' + str(request.patronyme))

        return response


def main():
    rclpy.init()

    full_name_service = FullNameService()

    rclpy.spin(full_name_service)

    rclpy.shutdown()


if __name__ == '__main__':
    main()
