#!/usr/bin/env python3
"""
End-Effector Pose Publisher Node
---------------------------------
Looks up the current transform from 'world' to 'end_effector' using TF2
and republishes it as a geometry_msgs/PoseStamped on /end_effector_pose.

Your task (TODO 2):
    Implement _publish_pose() so that:
    - It looks up the transform 'world' → 'end_effector' from the TF buffer
    - Converts the TransformStamped into a PoseStamped message
    - Publishes it on self._publisher at 10 Hz


Error handling requirements:
    - If the transform is not yet available, log a warning and return
      (do NOT crash or raise)
    - Handle at minimum: LookupException, ExtrapolationException,
      ConnectivityException
"""

import rclpy
from rclpy.node import Node


class PosePublisher(Node):
    def __init__(self):
        super().__init__('pose_publisher')
        self.get_logger().info('PosePublisher started.')


def main(args=None):
    rclpy.init(args=args)
    node = PosePublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
