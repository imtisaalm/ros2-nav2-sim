"""Launch the TurtleBot3 Burger in a Gazebo Harmonic world.

Usage:
    ros2 launch nav2_sim_demo sim.launch.py

This includes the official turtlebot3_gazebo world launch. The lighter
alternative world is empty_world.launch.py (same package).
"""
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    tb3_gazebo = get_package_share_directory('turtlebot3_gazebo')

    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(tb3_gazebo, 'launch', 'turtlebot3_world.launch.py')
            ),
        ),
    ])
