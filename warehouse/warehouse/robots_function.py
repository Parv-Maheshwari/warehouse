#! /usr/bin/env python
import rclpy
from rclpy.node import Node
# from rclpy.exceptions import ParameterNotDeclaredException
# from rcl_interfaces.msg import ParameterType
from std_msgs.msg import String
from my_robot_interfaces.msg import Robot
# from my_robot_interfaces.msg import Task


class robot(Node):
    def __init__(self):
        super().__init__('robot_node')

        self.declare_parameters(
            namespace='',
            parameters=[
                ('my_parameter', None),
            ])
        self.my_param = self.get_parameter('my_parameter').get_parameter_value().string_value

        self.publisher_ = self.create_publisher(Robot, 'topic_pubs%s' % self.my_param, 10)
        self.subscription = self.create_subscription(String,'orders',self.listener_callback,10)
        
        self.i =0
        self.subscription
        # timer_period = 2  # seconds
        # self.timer = self.create_timer(timer_period, self.timer_callback)
        # self.declare_parameter('my_parameter', 'world')

    def listener_callback(self,msg):
        # self.get_logger().info(f'Hello. Robot has to go from {msg.shelf_no} to {msg.picking_st_no}')
        msg1 = Robot()
        msg1.pos.x =float(self.my_param)
        msg1.pos.y = float(self.my_param)
        msg1.pos.z = float(self.my_param)
        msg1.battery = self.i%100
        self.publisher_.publish(msg1)
        self.get_logger().info('Publishing: %d' % msg1.battery)
        self.i+=1

def main():
    rclpy.init()
    node = robot()
    rclpy.spin(node)

if __name__ == '__main__':
    main()