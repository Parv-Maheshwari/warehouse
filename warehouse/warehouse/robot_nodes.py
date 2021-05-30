#! /usr/bin/env python
import rclpy
from rclpy.node import Node
# from rclpy.exceptions import ParameterNotDeclaredException
# from rcl_interfaces.msg import ParameterType
# from std_msgs.msg import String
from my_robot_interfaces.msg import Robot, ListTask, PosTask


class robot(Node):
    def __init__(self):
        super().__init__('robot_node')

        self.declare_parameters(
            namespace='',
            parameters=[
                ('my_parameter', None),
            ])
        self.my_param = self.get_parameter('my_parameter').get_parameter_value().string_value

        self.publisher_ = self.create_publisher(PosTask, 'cur_state%s' % self.my_param, 10)
        self.subscription_robot = self.create_subscription(Robot,'topic_pubs%s'% self.my_param,self.listener_callback_robot,10)
        self.subscription_tasks = self.create_subscription(ListTask,'new_tasks%s'% self.my_param,self.listener_callback_tasks,10)
        
        self.i =0
        self.subscription_robot

        self.tasks = ListTask().tasks

    def listener_callback_robot(self,msg):
        # self.get_logger().info(f'Hello. Robot has to go from {msg.shelf_no} to {msg.picking_st_no}')
        msg1 = PosTask()
        msg1.rinfo = msg
        print(type(self.tasks))
        print(type(msg1.tasks))
        msg1.tasks = self.tasks
        
        self.publisher_.publish(msg1)
        self.i+=1

    def listener_callback_tasks(self,msg):
        # self.get_logger().info(f'Hello. Robot has to go from {msg.shelf_no} to {msg.picking_st_no}')
        self.tasks = msg.tasks


def main():
    rclpy.init()
    node = robot()
    rclpy.spin(node)

if __name__ == '__main__':
    main()