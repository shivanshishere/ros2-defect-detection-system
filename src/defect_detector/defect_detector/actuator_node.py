import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class ActuatorNode(Node):
    def __init__(self):
        super().__init__('actuator_node')

        # Subscribe to actuator command topic
        self.subscription = self.create_subscription(
            String,
            'actuator_command',
            self.listener_callback,
            10
        )

    def listener_callback(self, msg):
        defect = msg.data
        self.get_logger().info(f"Actuator Node: Triggering action for {defect}")

        # Advanced logic based on defect priority
        high_priority_defects = ['crazing', 'rolled-in-scale']
        if defect in high_priority_defects:
            self.get_logger().info(f"[ACTUATOR] HIGH PRIORITY: Immediate action for {defect}")
        else:
            self.get_logger().info(f"[ACTUATOR] Normal action: Monitor {defect}")

        # TODO: Replace below with actual hardware commands
        # Example: GPIO HIGH, motor trigger, buzzer, robotic arm etc.

def main(args=None):
    rclpy.init(args=args)
    node = ActuatorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()