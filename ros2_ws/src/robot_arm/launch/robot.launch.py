import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    pkg_dir = get_package_share_directory('robot_arm')
    urdf_path = os.path.join(pkg_dir, 'urdf', 'robot_arm.urdf')

    with open(urdf_path, 'r') as f:
        robot_description = f.read()

    return LaunchDescription([

        # Publishes robot_description parameter + TF from URDF fixed joints
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': robot_description}],
        ),

        # TODO 1 — add your tf_publisher node here

        # TODO 2 — add your pose_publisher node here

    ])
