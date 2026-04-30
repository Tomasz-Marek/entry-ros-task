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

#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import PoseStamped
from tf2_ros import Buffer, TransformListener
from tf2_ros import LookupException, ExtrapolationException, ConnectivityException


class PosePublisher(Node):
    def __init__(self):
        super().__init__('pose_publisher')
        self.get_logger().info('PosePublisher started.')

        self._tf_buffer = Buffer()
        self._tf_listener = TransformListener(self._tf_buffer, self)

        self._publisher = self.create_publisher(
            PoseStamped,
            '/end_effector_pose',
            10
        )

        # 10 Hz = co 0.1 s
        self._timer = self.create_timer(0.1, self._publish_pose)

    def _publish_pose(self):
        try:
            transform = self._tf_buffer.lookup_transform(
                'world',
                'end_effector',
                rclpy.time.Time()
            )

        except (LookupException, ExtrapolationException, ConnectivityException) as error:
            self.get_logger().warn(
                f'Could not transform world to end_effector: {error}'
            )
            return

        pose_msg = PoseStamped()
        pose_msg.header = transform.header

        pose_msg.pose.position.x = transform.transform.translation.x
        pose_msg.pose.position.y = transform.transform.translation.y
        pose_msg.pose.position.z = transform.transform.translation.z

        pose_msg.pose.orientation = transform.transform.rotation

        self._publisher.publish(pose_msg)


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