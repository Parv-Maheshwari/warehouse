import unittest
import pytest
import os
from ament_index_python.packages import get_package_share_directory
import yaml

class TestClass:
    def test_params(self):
        # x = "this"

        config1 = os.path.join(
        get_package_share_directory('warehouse'),
        'config',
        'task_allocator.yaml'
        )
        config2 = os.path.join(
        get_package_share_directory('warehouse'),
        'config',
        'tasks.yaml'
        )
        print(config1)
        with open(config1) as file:
            documents = yaml.full_load(file)
            robot_no = documents['task_allocator']['ros__parameters']['robot_no']
            alpha = documents['task_allocator']['ros__parameters']['alpha']

        with open(config2) as file:
            documents = yaml.full_load(file)
            no_of_shelf = documents['task']['ros__parameters']['no_of_shelf']
            shelf_init_pos_row = documents['task']['ros__parameters']['shelf_init_pos_row']
            shelf_init_pos_col = documents['task']['ros__parameters']['shelf_init_pos_col']
            no_of_picking_stations = documents['task']['ros__parameters']['no_of_picking_stations']
            pos_of_picking_stations_row = documents['task']['ros__parameters']['pos_of_picking_stations_row']
            pos_of_picking_stations_col = documents['task']['ros__parameters']['pos_of_picking_stations_col']

        # print(robot_no)
        assert type(robot_no) is int and robot_no>0

        assert (type(alpha) is int or float) and 0<=alpha<=1

        assert type(no_of_shelf) is int and no_of_shelf>0

        assert type(shelf_init_pos_row) is list and len(shelf_init_pos_row) == no_of_shelf and (all((isinstance(item, float) or isinstance(item, int) )for item in shelf_init_pos_row))

        assert type(shelf_init_pos_col) is list and len(shelf_init_pos_col) == no_of_shelf and (all((isinstance(item, float) or isinstance(item, int) )for item in shelf_init_pos_col))
        
        assert type(no_of_picking_stations) is int and no_of_picking_stations>0

        assert type(pos_of_picking_stations_row) is list and len(pos_of_picking_stations_row) == no_of_picking_stations and (all((isinstance(item, float) or isinstance(item, int) )for item in pos_of_picking_stations_row))

        assert type(pos_of_picking_stations_col) is list and len(pos_of_picking_stations_col) == no_of_picking_stations and (all((isinstance(item, float) or isinstance(item, int) )for item in pos_of_picking_stations_col))
    # def test_two(self):
        # x = "hello"
        # assert hasattr(x, "check")