from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # Node(
        #     package='warehouse',
        #     executable='robots',
        #     name='robot1',
        #     output='screen',
        #     emulate_tty=True,
        #     parameters=[
        #         {'my_parameter': '1'}, {'opp_parameter': '2'}
        #     ]
        # ),
        Node(
            package='warehouse',
            executable='robots',
            name='robot2',
            output='screen',
            emulate_tty=True,
            parameters=[
                {'my_parameter': '2'}, {'opp_parameter': '1'}
            ]
        )
    ])
