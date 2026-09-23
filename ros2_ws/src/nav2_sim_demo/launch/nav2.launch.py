"""Run the Nav2 stack on a previously saved map for autonomous navigation.

Usage:
    ros2 launch nav2_sim_demo nav2.launch.py
    ros2 launch nav2_sim_demo nav2.launch.py map:=/path/to/other_map.yaml

Run this AFTER sim.launch.py is up AND you have saved a map with
`ros2 run nav2_map_server map_saver_cli` (see docs/checklist.md Phase 3).

The default params file is the TurtleBot3-tuned one shipped with nav2_bringup.
Verify it exists on your machine with:
    ls $(ros2 pkg prefix nav2_bringup)/share/nav2_bringup/params/
"""
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    pkg_share = get_package_share_directory('nav2_sim_demo')
    nav2_bringup = get_package_share_directory('nav2_bringup')

    default_map = os.path.join(pkg_share, 'maps', 'tb3_world.yaml')
    default_params = os.path.join(nav2_bringup, 'params', 'nav2_params.yaml')

    return LaunchDescription([
        DeclareLaunchArgument(
            'map',
            default_value=default_map,
            description='Full path to the saved map YAML file'),
        DeclareLaunchArgument(
            'params_file',
            default_value=default_params,
            description='Full path to the Nav2 params file'),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(nav2_bringup, 'launch', 'bringup_launch.py')
            ),
            launch_arguments={
                'map': LaunchConfiguration('map'),
                'params_file': LaunchConfiguration('params_file'),
                'use_sim_time': 'true',
            }.items(),
        ),
    ])
