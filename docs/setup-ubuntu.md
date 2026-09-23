# Setup: Path C (native Ubuntu 24.04)

For a native Linux machine or WSL2. If your main machine is the Mac, use Path A (UTM VM) instead.

This is the recommended path. ROS 2 Jazzy targets Ubuntu 24.04 directly, so everything installs with `apt` and the Gazebo GUI runs at full speed.

## What you need

- A machine running Ubuntu 24.04 (Noble). This can be your main OS, a dual-boot, or a dedicated machine.
- 8 GB RAM minimum, 20 GB free disk.
- Internet access. The install downloads a few GB.

## Install

One script does everything: ROS 2 Jazzy desktop, Gazebo Harmonic, the ROS-Gazebo bridge, TurtleBot3 packages, Nav2, SLAM Toolbox, and colcon.

```bash
cd ~/ros2-nav2-sim   # or wherever you cloned this repo
bash scripts/install-jazzy.sh
```

It takes 20-40 minutes, mostly downloading. When it finishes:

```bash
# close the terminal, open a new one, then:
echo $ROS_DISTRO        # expect: jazzy
echo $TURTLEBOT3_MODEL  # expect: burger
```

Both lines print correctly? Move on to `docs/checklist.md`, Phase 1.

## What the script does (so nothing is magic)

1. Confirms you are on Ubuntu 24.04
2. Adds the official ROS 2 apt repository (same steps as the [official install docs](https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html))
3. Installs `ros-jazzy-desktop` (ROS 2 plus RViz and GUI tools)
4. Installs `gz-harmonic` (Gazebo Harmonic) and `ros-jazzy-ros-gz` (the bridge between ROS 2 and Gazebo)
5. Installs `ros-jazzy-turtlebot3*`, `ros-jazzy-navigation2`, `ros-jazzy-nav2-bringup`, `ros-jazzy-slam-toolbox`, and colcon
6. Appends the two `source`/`export` lines to your `~/.bashrc` (only if they are missing)

## Troubleshooting

**`$ROS_DISTRO` is empty.** You skipped the "close the terminal, open a new one" step. `~/.bashrc` only loads in new terminals.

**Gazebo opens to a gray void on first launch.** It downloads 3D models the first time. Give it 5 minutes, then close and relaunch.

**`ros2` command not found.** The install script failed partway. Scroll up in its output for the first red error, fix that, and re-run the script. It is safe to re-run.

**Everything is slow.** Gazebo wants a real GPU for the 3D view, but it still runs on integrated graphics, just with lower frame rates. The robot logic (SLAM, Nav2) runs fine on CPU. Lower the Gazebo render resolution if needed: in the Gazebo GUI, it still simulates correctly even when the 3D view stutters.
