import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool


class ToggleClient(Node):

    def __init__(self):
        super().__init__('toggle_client')

        self.client = self.create_client(SetBool, 'toggle_movement')

        # wait for the server to come up
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for /toggle_movement service...')

        # one-shot timer: after 5 seconds, call the service once
        self.delay_timer = self.create_timer(5.0, self.send_request)
        self.called = False

    def send_request(self):
        if self.called:
            return
        self.called = True

        req = SetBool.Request()
        req.data = True

        self.future = self.client.call_async(req)
        self.future.add_done_callback(self.on_response)
        self.get_logger().info('Sent SetBool(data=True) request')

    def on_response(self, future):
        try:
            response = future.result()
            self.get_logger().info(
                f'Service replied: success={response.success}, message="{response.message}"'
            )
        except Exception as e:
            self.get_logger().error(f'Service call failed: {e}')


def main():
    rclpy.init()
    node = ToggleClient()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()