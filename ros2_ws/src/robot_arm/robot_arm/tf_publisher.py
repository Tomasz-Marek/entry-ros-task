#!/usr/bin/env python3
"""
TF Publisher Node
-----------------
Publishes the TF2 transform chain for a 2-DOF robot arm.

Chain layout:
    world
      └── base_link       (static, identity)
            └── link1     (dynamic, rotates around Z over time)
                  └── link2  (static offset: x=0.3m from link1)
                        └── end_effector  (static offset: x=0.2m from link2)

Your task (TODO 1):
    Implement the _broadcast() method so that:
    - 'world' → 'base_link'       is a static identity transform
    - 'base_link' → 'link1'       rotates around Z with amplitude 45° (0.785 rad)
                                  at a frequency of 0.5 Hz
    - 'link1' → 'link2'           is a static transform with x=0.3m offset
    - 'link2' → 'end_effector'    is a static transform with x=0.2m offset

    Use StaticTransformBroadcaster for transforms that never change.
    Use TransformBroadcaster for transforms that change over time.
"""

import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster, StaticTransformBroadcaster
class TFPublisher(Node):

    def __init__(self):
        super().__init__('tf_publisher')
        self.get_logger().info('TFPublisher started.')

        self.dynamic_broadcaster = TransformBroadcaster(self)
        self.static_broadcaster = StaticTransformBroadcaster(self)

        self.start_time = self.get_clock().now()

        self.broadcast_static_transforms()

        # 50 Hz = co 0.02 s
        self.timer = self.create_timer(0.02, self.broadcast_dynamic_transform)

    def broadcast_static_transforms(self):
        static_transforms = [
            self.create_transform(
                parent_frame='world',
                child_frame='base_link',
                x=0.0,
                y=0.0,
                z=0.0,
                yaw=0.0
            ),
            self.create_transform(
                parent_frame='link1',
                child_frame='link2',
                x=0.3,
                y=0.0,
                z=0.0,
                yaw=0.0
            ),
            self.create_transform(
                parent_frame='link2',
                child_frame='end_effector',
                x=0.2,
                y=0.0,
                z=0.0,
                yaw=0.0
            ),
        ]

        self.static_broadcaster.sendTransform(static_transforms)

    def broadcast_dynamic_transform(self):
        elapsed_time = (self.get_clock().now() - self.start_time).nanoseconds / 1e9

        amplitude = math.radians(45.0)
        frequency = 0.5

        angle = amplitude * math.sin(2.0 * math.pi * frequency * elapsed_time)

        transform = self.create_transform(
            parent_frame='base_link',
            child_frame='link1',
            x=0.0,
            y=0.0,
            z=0.0,
            yaw=angle
        )

        self.dynamic_broadcaster.sendTransform(transform)

    def create_transform(self, parent_frame, child_frame, x, y, z, yaw):
        transform = TransformStamped()

        transform.header.stamp = self.get_clock().now().to_msg()
        transform.header.frame_id = parent_frame
        transform.child_frame_id = child_frame

        transform.transform.translation.x = x
        transform.transform.translation.y = y
        transform.transform.translation.z = z

        transform.transform.rotation.x = 0.0
        transform.transform.rotation.y = 0.0
        transform.transform.rotation.z = math.sin(yaw / 2.0)
        transform.transform.rotation.w = math.cos(yaw / 2.0)

        return transform


def main(args=None):
    rclpy.init(args=args)
    node = TFPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()