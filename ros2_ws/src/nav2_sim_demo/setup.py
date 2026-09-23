from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'nav2_sim_demo'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.py'))),
        (os.path.join('share', package_name, 'maps'), glob(os.path.join('maps', '*'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Imtisaal Mian',
    maintainer_email='imtisaal@thelabzero.org',
    description='TurtleBot3 Gazebo Harmonic sim: teleop, SLAM mapping, Nav2 waypoint missions.',
    license='MIT',
    entry_points={
        'console_scripts': [
        ],
    },
)
