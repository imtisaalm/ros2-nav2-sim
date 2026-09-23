#!/usr/bin/env bash
# Install ROS 2 Jazzy + Gazebo Harmonic + TurtleBot3 + Nav2 + SLAM Toolbox
# on Ubuntu 24.04 (amd64 or arm64). Safe to re-run.
set -euo pipefail

echo "=== Checking Ubuntu version ==="
if ! grep -q 'VERSION_ID="24.04"' /etc/os-release; then
    echo "This script is for Ubuntu 24.04 only. Found:"
    grep PRETTY_NAME /etc/os-release
    exit 1
fi
echo "Ubuntu 24.04 confirmed."

echo "=== Locale ==="
sudo apt update
sudo apt install -y locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8

echo "=== ROS 2 apt repository ==="
sudo apt install -y software-properties-common curl
sudo add-apt-repository -y universe
ROS_APT_SOURCE_VERSION=$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | grep -F "tag_name" | awk -F\" '{print $4}')
curl -L -o /tmp/ros2-apt-source.deb "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. /etc/os-release && echo ${UBUNTU_CODENAME:-${VERSION_CODENAME}})_all.deb"
sudo dpkg -i /tmp/ros2-apt-source.deb

echo "=== ROS 2 Jazzy desktop ==="
sudo apt update
sudo apt install -y ros-jazzy-desktop

echo "=== Gazebo Harmonic + ROS bridge ==="
sudo apt install -y gz-harmonic
sudo apt install -y ros-jazzy-ros-gz

echo "=== TurtleBot3 + Nav2 + SLAM Toolbox + colcon ==="
sudo apt install -y "ros-jazzy-turtlebot3*"
sudo apt install -y ros-jazzy-navigation2 ros-jazzy-nav2-bringup
sudo apt install -y ros-jazzy-slam-toolbox
sudo apt install -y python3-colcon-common-extensions

echo "=== Shell setup (adds lines to ~/.bashrc if missing) ==="
append_once() { grep -qxF "$1" ~/.bashrc || echo "$1" >> ~/.bashrc; }
append_once 'source /opt/ros/jazzy/setup.bash'
append_once 'export TURTLEBOT3_MODEL=burger'

echo ""
echo "=== Done ==="
echo "Close this terminal, open a new one, then run:"
echo "  echo \$ROS_DISTRO        # expect: jazzy"
echo "  echo \$TURTLEBOT3_MODEL  # expect: burger"
echo "Then continue with docs/checklist.md Phase 1."
