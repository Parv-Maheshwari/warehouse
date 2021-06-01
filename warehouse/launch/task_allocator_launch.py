from launch import LaunchDescription
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    config = os.path.join(
    get_package_share_directory('warehouse'),
    'config',
    'task_allocator.yaml'
    )
    return LaunchDescription([
        Node(
            package='warehouse',
            executable='tasks_allocator',
            name='task_allocator',
            output='screen',
            emulate_tty=True,
            parameters=[
                config
            ]
        ),
    ])
