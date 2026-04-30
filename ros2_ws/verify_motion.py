#!/usr/bin/env python3

import math
import time

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped


class MotionVerifier(Node):
    def __init__(self):
        super().__init__('motion_verifier')

        self.first_position = None
        self.max_distance = 0.0
        self.samples = 0
        self.finished = False

        self.subscription = self.create_subscription(
            PoseStamped,
            '/end_effector_pose',
            self.callback,
            10
        )

    def callback(self, msg):
        pos = msg.pose.position
        current = (pos.x, pos.y)

        if self.first_position is None:
            self.first_position = current
            self.get_logger().info('Initial position saved')
            return

        dx = current[0] - self.first_position[0]
        dy = current[1] - self.first_position[1]
        distance = math.sqrt(dx*dx + dy*dy)

        self.max_distance = max(self.max_distance, distance)
        self.samples += 1

        self.get_logger().info(
            f'Samples: {self.samples}, max movement: {self.max_distance:.4f}'
        )

        if self.samples >= 20:
            if self.max_distance > 0.05:
                self.get_logger().info('SUCCESS: Arm is moving')
            else:
                self.get_logger().error('FAILURE: Arm is NOT moving')

            self.finished = True


def main():
    rclpy.init()
    node = MotionVerifier()

    try:
        while rclpy.ok() and not node.finished:
            rclpy.spin_once(node)
            time.sleep(0.01)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
