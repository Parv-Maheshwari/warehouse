import os
from glob import glob
from setuptools import setup

package_name = 'warehouse'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name), glob('launch/*.py')),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml'))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='drago',
    maintainer_email='parvmaheshwari2002@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'robots = warehouse.robots_function:main',
            'tasks = warehouse.tasks:main',
            'robots_node = warehouse.robot_nodes:main',
            'tasks_allocator = warehouse.task_allocator:main'
        ],
    },
)
