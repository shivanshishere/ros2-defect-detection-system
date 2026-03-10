import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class DecisionNode(Node):
    def __init__(self):
        super().__init__('decision_node')

        # Subscriber: inference node predictions
        self.subscription = self.create_subscription(
            String,
            'defect_prediction',
            self.listener_callback,
            10
        )

        # Publisher: actuator command topic
        self.actuator_pub = self.create_publisher(String, 'actuator_command', 10)

        # Defect priorities
        self.defect_priorities = {
            'scratches': 3,
            'crazing': 5,
            'rolled-in-scale': 4,
            'inclusion': 2,
            'patches': 1,
            'pitted_surface': 2
        }

        # Cooldown timer for actuator
        self.last_trigger_time = 0
        self.cooldown_seconds = 3

    def listener_callback(self, msg):
        defect = msg.data
        self.get_logger().info(f"Decision Node: Received {defect}")

        import time
        current_time = time.time()
        priority = self.defect_priorities.get(defect, 0)

        # Check cooldown
        if current_time - self.last_trigger_time < self.cooldown_seconds:
            self.get_logger().info("Decision Node: Cooldown active, skipping trigger")
            return

        if priority > 0:
            self.publish_actuator_command(defect)
            self.last_trigger_time = current_time

    def publish_actuator_command(self, defect):
        msg = String()
        msg.data = defect
        self.actuator_pub.publish(msg)
        self.get_logger().info(f"Decision Node: Published actuator command for {defect}")


def main(args=None):
    rclpy.init(args=args)
    node = DecisionNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()