"""Run SLAM Toolbox (online async) against the running simulation.

Usage:
    ros2 launch nav2_sim_demo mapping.launch.py

Run this AFTER sim.launch.py is up. Drive the robot with
`ros2 run turtlebot3_teleop teleop_keyboard` and watch the map build in RViz.
"""
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    slam_toolbox = get_package_share_directory('slam_toolbox')

    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(slam_toolbox, 'launch', 'online_async_launch.py')
            ),
            launch_arguments={'use_sim_time': 'true'}.items(),
        ),
    ])
