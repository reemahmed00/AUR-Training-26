import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    package_share = get_package_share_directory('session2')
    param_file = os.path.join(package_share, 'config', 'go_to_goal_params.yaml')

    return LaunchDescription([
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='turtlesim',
            output='screen',
        ),
        Node(
            package='session2',
            executable='go_to_goal_server',
            name='go_to_goal_server',
            parameters=[param_file],
            output='screen',
        ),
        Node(
            package='session2',
            executable='client',
            name='toggle_client',
            output='screen',
        ),
    ])