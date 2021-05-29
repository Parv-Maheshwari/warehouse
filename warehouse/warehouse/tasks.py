#! /usr/bin/env python
import rclpy
from rclpy.node import Node
# from rclpy.exceptions import ParameterNotDeclaredException
# from rcl_interfaces.msg import ParameterType
from std_msgs.msg import String
from my_robot_interfaces.msg import Task
import random


class task(Node):
    def __init__(self):
        super().__init__('task_node')

        # self.declare_parameter('my_parameter', '0')
        # self.declare_parameter('opp_parameter', '0')
        self.declare_parameters(
        namespace='',
        parameters=[
            ('no_of_shelf', None),
            ('shelf_init_pos_row', None),
            ('shelf_init_pos_col', None),
            ('no_of_picking_stations', None),
            ('pos_of_picking_stations_row', None),
            ('pos_of_picking_stations_col', None),
        ])

        self.no_of_shelf = self.get_parameter('no_of_shelf').get_parameter_value().integer_value
        self.shelf_init_pos_row = self.get_parameter('shelf_init_pos_row').get_parameter_value().integer_array_value
        self.shelf_init_pos_col = self.get_parameter('shelf_init_pos_col').get_parameter_value().integer_array_value
        self.no_of_picking_stations = self.get_parameter('no_of_picking_stations').get_parameter_value().integer_value
        self.pos_of_picking_stations_row = self.get_parameter('pos_of_picking_stations_row').get_parameter_value().integer_array_value
        self.pos_of_picking_stations_col = self.get_parameter('pos_of_picking_stations_col').get_parameter_value().integer_array_value

        self.shelf_pos=[]
        self.picking_stations_pos=[]
        for i in range(self.no_of_shelf):
            self.shelf_pos.append((self.shelf_init_pos_row[i],self.shelf_init_pos_col[i]))
        for j in range(self.no_of_picking_stations):
            self.picking_stations_pos.append((self.pos_of_picking_stations_row[j],self.pos_of_picking_stations_col[j]))
        
        # print(self.shelf_pos)
        # print(self.picking_stations_pos)
        # print(f"fffffffffffff{self.shelf_init_pos_row[0]}")
        # self.opp_param = self.get_parameter('opp_parameter').get_parameter_value().string_value

        self.publisher_ = self.create_publisher(Task, 'tasks', 10)
        self.subscription = self.create_subscription(String,'orders',self.listener_callback,10)
        
        self.i =0
        self.subscription
        # timer_period = 2  # seconds
        # self.timer = self.create_timer(timer_period, self.timer_callback)
        # self.declare_parameter('my_parameter', 'world')

    def listener_callback(self,msg):
        # self.get_logger().info('Hello from robot at %f %f %f!' % (msg.pos.x,msg.pos.y,msg.pos.z))
        msg1 = Task()

        msg1.id = self.i
        
        msg1.shelf_no = random.randint(1, self.no_of_shelf)-1
        shelf = self.shelf_pos[msg1.shelf_no]
        self.get_logger().info(f'Selected {msg1.shelf_no} at {shelf}')
        msg1.shelf_pos.x = float(shelf[0])
        msg1.shelf_pos.y = float(shelf[1])
        msg1.shelf_pos.z = 0.

        msg1.picking_st_no = random.randint(1, self.no_of_picking_stations)-1
        picking_st = self.picking_stations_pos[msg1.picking_st_no]
        self.get_logger().info(f'Selected {msg1.picking_st_no} at {picking_st}')
        msg1.picking_station_pos.x = float(picking_st[0])
        msg1.picking_station_pos.y = float(picking_st[1])
        msg1.picking_station_pos.z = 0.

        self.publisher_.publish(msg1)
        self.get_logger().info(f'Publishing: from {msg1.shelf_no} to {msg1.picking_st_no}')
        self.i+=1

def main():
    rclpy.init()
    node = task()
    rclpy.spin(node)

if __name__ == '__main__':
    main()