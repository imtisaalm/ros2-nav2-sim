# First-demo checklist

One tiny step at a time. Check each box as you go. If a step fails, stop there and read the troubleshooting note before moving on.

## Phase 0: Pick your path (5 minutes)

You are on a Mac. Your options, best first:

- [ ] **Path A: UTM VM on your Mac** (recommended, $0) → follow `docs/setup-mac.md`
- [ ] **Path B: Remote Linux over SSH** (~$5-10 USD/month, full-speed sim) → follow `docs/setup-remote.md`
- [ ] **Path C: Native Ubuntu 24.04** (only if you have a Linux machine or WSL2) → follow `docs/setup-ubuntu.md`
- [ ] I finished my path's setup guide and ROS 2 is installed

## Phase 1: Build the demo workspace

Do this once. Afterwards you only repeat the `source` line in each new terminal.

- [ ] Open a terminal
- [ ] `cd` into the repo: `cd ~/ros2-nav2-sim` (or wherever you cloned it)
- [ ] `cd ros2_ws`
- [ ] Build: `colcon build --symlink-install`
- [ ] Wait for it to finish. You should see `Summary: 1 package finished`
- [ ] Source it: `source install/setup.bash`
- [ ] Verify: `ros2 pkg list | grep nav2_sim_demo` → you see `nav2_sim_demo`

From now on, every new terminal needs two lines before ROS commands work:

```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2-nav2-sim/ros2_ws/install/setup.bash
```

(Path B: run these *inside* the container instead. `/opt/ros/jazzy/setup.bash` is already sourced there.)

## Phase 2: Drive it (teleop)

Goal: see the robot move in the sim.

- [ ] Terminal 1: `ros2 launch nav2_sim_demo sim.launch.py`
- [ ] Wait. Gazebo opens with a TurtleBot3 Burger in a walled world. First launch downloads models, so it can take a few minutes.
- [ ] Terminal 2 (new terminal, source both lines first): `ros2 run turtlebot3_teleop teleop_keyboard`
- [ ] Click into Terminal 2 so it has keyboard focus
- [ ] Press `i` → the robot drives forward in Gazebo
- [ ] Press `k` → the robot stops
- [ ] Press `j` and `l` → the robot turns
- [ ] Drive around for 2 minutes. Done when moving the robot feels boring.

Keys: `i` forward, `,` back, `j` left, `l` right, `k` stop.

Troubleshooting: if the robot ignores you, Terminal 2 lost keyboard focus. Click it and try again. If Gazebo shows an empty gray world, wait longer on first launch.

## Phase 3: Map it (SLAM)

Goal: the robot draws a 2D map of the world as you drive.

- [ ] Terminal 1: `ros2 launch nav2_sim_demo sim.launch.py` (Gazebo running)
- [ ] Terminal 2 (sourced): `ros2 launch nav2_sim_demo mapping.launch.py`
- [ ] Terminal 3 (sourced): `ros2 run rviz2 rviz2`
- [ ] In RViz, set **Fixed Frame** (top left) to `map`
- [ ] Click **Add** (bottom left) → **By topic** tab → expand `/map` → select **Map** → OK
- [ ] You see a partial gray map. Good, SLAM is listening.
- [ ] Terminal 4 (sourced): `ros2 run turtlebot3_teleop teleop_keyboard`
- [ ] Drive **slowly** around the whole world. Short forward bursts, gentle turns. Fast driving makes blurry maps.
- [ ] Watch the map fill in inside RViz. Keep going until the walls look complete.
- [ ] Terminal 5 (sourced): `ros2 run nav2_map_server map_saver_cli -f ~/ros2-nav2-sim/ros2_ws/src/nav2_sim_demo/maps/tb3_world`
- [ ] Verify: `ls ~/ros2-nav2-sim/ros2_ws/src/nav2_sim_demo/maps/` shows `tb3_world.pgm` and `tb3_world.yaml`
- [ ] Open the `.pgm` file in an image viewer. You should recognize the world layout.
- [ ] Close Terminals 1-4 with Ctrl+C. Mapping is done.

Troubleshooting: if RViz shows nothing under `/map`, check Fixed Frame is `map` and that mapping.launch.py is still running without errors.

## Phase 4: Send it on missions (Nav2)

Goal: click a goal in RViz and watch the robot drive itself there.

- [ ] Terminal 1 (sourced): `ros2 launch nav2_sim_demo sim.launch.py`
- [ ] Terminal 2 (sourced): `ros2 launch nav2_sim_demo nav2.launch.py`
- [ ] Wait ~30 seconds. Nav2 brings up a dozen nodes; the terminal fills with startup logs and then goes quiet.
- [ ] Terminal 3 (sourced): `ros2 run rviz2 rviz2`
- [ ] In RViz: Fixed Frame → `map`. Add → By topic → `/map` → Map.
- [ ] You see your saved map with the robot sitting somewhere wrong. That is expected.
- [ ] Click **2D Pose Estimate** in the RViz toolbar. Click on the map where the robot actually starts, drag in the direction it faces, release.
- [ ] A cloud of green arrows appears and tightens around the robot. Wait until it looks settled (10-20 seconds).
- [ ] Click **2D Nav Goal** in the toolbar. Click a spot across the map, drag to set the facing direction, release.
- [ ] The robot plans a path (green line) and drives there on its own.
- [ ] Send a second goal somewhere else. Then a third.

Troubleshooting: if the robot spins in place or the plan looks crazy, the initial pose estimate was off. Click **2D Pose Estimate** again and re-do it. If Nav2 errors on startup, check the map files exist from Phase 3.

## Phase 5: Show it

- [ ] Follow `docs/screen-capture.md` and record your demo
- [ ] Fill in `docs/writeup-template.md`
- [ ] Push your writeup and video link to this repo

Done. You now have a public artifact proving you can stand up a ROS 2 autonomy stack.
