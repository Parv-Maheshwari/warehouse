from launch import LaunchDescription
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory
import yaml

def generate_launch_description():
    config = os.path.join(
    get_package_share_directory('warehouse'),
    'config',
    'task_allocator.yaml'
    )
    with open(config) as file:
        documents = yaml.full_load(file)
        robot_no = documents['task_allocator']['ros__parameters']['robot_no']
    robots_node =[]
    for i in range(robot_no):
        robots_node.append(
        Node(
            package='warehouse',
            executable='robots_node',
            name=f'robot{i}node',
            output='screen',
            emulate_tty=True,
            parameters=[
                {'my_parameter': f'{i}'}
            ]
        ))
    return LaunchDescription(robots_node)
