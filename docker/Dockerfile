# Fallback only: ROS 2 Jazzy + Gazebo Harmonic container.
# On Apple Silicon the Gazebo/RViz GUIs fail (documented), so this path is
# here for headless use and for Linux hosts. See docs/setup-docker.md.
FROM osrf/ros:jazzy-desktop-full

ENV DEBIAN_FRONTEND=noninteractive \
    TURTLEBOT3_MODEL=burger

RUN apt-get update && apt-get install -y --no-install-recommends \
    gz-harmonic \
    ros-jazzy-ros-gz \
    "ros-jazzy-turtlebot3*" \
    ros-jazzy-navigation2 \
    ros-jazzy-nav2-bringup \
    ros-jazzy-slam-toolbox \
    python3-colcon-common-extensions \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /root/ros2_ws
