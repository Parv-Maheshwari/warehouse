#! /usr/bin/env python
import rclpy
from rclpy.node import Node
# from rclpy.exceptions import ParameterNotDeclaredException
# from rcl_interfaces.msg import ParameterType
from std_msgs.msg import String
from my_robot_interfaces.msg import Task, PosTask, ListTask
import copy

def ass_cost(task1, task2):
    return abs(task1.shelf_pos.x - task2.shelf_pos.x) + abs(task1.shelf_pos.y - task2.shelf_pos.y)

def own_cost(task1):
    return 2* (abs(task1.shelf_pos.x - task1.picking_station_pos.x) + abs(task1.shelf_pos.y - task1.picking_station_pos.y) )

class task_allocator(Node):
    def __init__(self):
        super().__init__('task_allocator_node')
        self.robot_no = 2
        self.publisher = [None] * self.robot_no
        self.subscription_cur_state = [None] * self.robot_no
        self.tasks = [None] * self.robot_no
        # self.publisher_ = self.create_publisher(Task, 'tasks', 10)
        for i in range(self.robot_no):
            self.publisher[i] = self.create_publisher(ListTask, f'new_tasks{i}', 10)
            self.tasks[i] = ListTask().tasks
            print(len(self.tasks[i]))


        self.subscription = self.create_subscription(Task,'tasks',self.listener_callback,10)
        self.subscription_cur_state[0] = self.create_subscription(PosTask,'cur_state0',self.listener_callback_cur_state_robot0,10)
        self.subscription_cur_state[1] = self.create_subscription(PosTask,'cur_state1',self.listener_callback_cur_state_robot1,10)

        self.subscription
        self.robot_temp_tasks = [None] * self.robot_no
        self.robot_temp_time_bid = [None] * self.robot_no
        self.robot_distance_bid = [None] * self.robot_no
        self.robot_time_bid = [None] * self.robot_no
        self.robot_total_bid = [None] * self.robot_no
        self.alpha = 0

    def listener_callback(self,msg):
        #########################################

        for i in range(self.robot_no):
            self.robot_distance_bid[i] = 0
            self.robot_temp_tasks[i] = 0
            if len(self.tasks[i])>0:
                self.robot_distance_bid[i] = ass_cost(msg,self.tasks[i][-1])

                for j in range(len(self.tasks[i])-1):
                    self.robot_temp_tasks[i] += own_cost(self.tasks[i][j]) + ass_cost(self.tasks[i][j], self.tasks[i][j+1])
                self.robot_temp_tasks[i] += own_cost(self.tasks[i][-1])
            print(f'robot {i} original current cost is : {self.robot_temp_tasks[i]}.')

        for i in range(self.robot_no):
            self.robot_temp_time_bid = copy.deepcopy(self.robot_temp_tasks)
            self.robot_temp_time_bid[i] += own_cost(msg)
            if len(self.tasks[i])>0:
                self.robot_temp_time_bid[i] += ass_cost(msg,self.tasks[i][-1])
            
            self.robot_time_bid[i] = max(self.robot_temp_time_bid)
            self.robot_total_bid[i] = self.alpha * self.robot_distance_bid[i] + (1-self.alpha) * self.robot_time_bid[i]
            print(f'robot {i} bids : {self.robot_total_bid[i]}.' )
        
        min_bid = min(self.robot_total_bid)
        robot_chosen = self.robot_total_bid.index(min_bid)
        print(f'robot {robot_chosen} is chosen.' )



        ######################################### 

        #################################### Working Comment out the below lines for simple task allocation
        # if msg.id%2 == 0:
        #     robot_chosen = 0
        # else:
        #     robot_chosen = 1
        
        # print(f'robot {robot_chosen} has tasks of length : {len(self.tasks[robot_chosen])}' )
        # print(f'robot {not robot_chosen} has tasks of length : {len(self.tasks[not robot_chosen])}' )

        self.tasks[robot_chosen].append(msg)

        # print(f'robot {robot_chosen} has tasks of length : {len(self.tasks[robot_chosen])}' )
        # print(f'robot {not robot_chosen} has tasks of length : {len(self.tasks[not robot_chosen])}' )

        # for i in range(self.robot_no):
        #     print(f'robot {i} has tasks of length : {len(self.tasks[i])}' )
        
        msg1 = ListTask()
        msg1.tasks = self.tasks[robot_chosen]
        self.publisher[robot_chosen].publish(msg1)

    def listener_callback_cur_state_robot0(self,msg):
        # self.get_logger().info(f'Hello. Robot has to go from {msg.shelf_no} to {msg.picking_st_no}')
        # self.get_logger().info(f'Publishing: {len(msg.tasks)}')
        # print(len(msg.tasks))
        self.tasks[0] = msg.tasks
    
    def listener_callback_cur_state_robot1(self,msg):
        # self.get_logger().info(f'Hello. Robot has to go from {msg.shelf_no} to {msg.picking_st_no}')
        self.get_logger().info(f'Publishing: {len(msg.tasks)}')
        # print(len(msg.tasks))
        self.tasks[1] = msg.tasks

def main():
    rclpy.init()
    node = task_allocator()
    rclpy.spin(node)

if __name__ == '__main__':
    main()