import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import tensorflow as tf
import numpy as np
import cv2
import os


class InferenceNode(Node):

    def __init__(self):
        super().__init__('inference_node')

        self.publisher = self.create_publisher(String, 'defect_prediction', 10)

        model_path = os.path.join(os.path.dirname(__file__), 'defect_model.h5')
        self.model = tf.keras.models.load_model(model_path)

        self.class_names = [
            'crazing',
            'inclusion',
            'patches',
            'pitted_surface',
            'rolled-in_scale',
            'scratches'
        ]

        self.timer = self.create_timer(3.0, self.predict_defect)

    def predict_defect(self):

        img_path = "/mnt/c/Users/Shivansh/Pictures/Screenshots/Screenshot (19).png"

        img = cv2.imread(img_path)
        img = cv2.resize(img, (224, 224))
        img = np.expand_dims(img, axis=0)

        prediction = self.model.predict(img)
        class_id = np.argmax(prediction)
        result = self.class_names[class_id]

        msg = String()
        msg.data = result

        self.publisher.publish(msg)

        self.get_logger().info(f"Prediction: {result}")


def main(args=None):

    rclpy.init(args=args)

    node = InferenceNode()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()