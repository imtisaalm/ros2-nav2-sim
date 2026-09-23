# Setup: remote Linux over SSH (alternative path)

Yes, this is real: you rent a small Linux computer in the cloud, SSH into it from your Mac terminal, and run the entire ROS 2 stack there. Your Mac just becomes a keyboard, screen, and browser.

## Honest comparison before you choose

| | UTM VM (primary) | Remote SSH (this guide) | Docker | RoboStack native |
|---|---|---|---|---|
| Cost | $0 | ~$5-10 USD/month while it exists ($0 option below) | $0 | $0 |
| GUI | RViz fine, Gazebo 3D slow | Foxglove in browser, works well | Gazebo/RViz GUIs fail on Apple Silicon | Fragile bridge, not beginner-safe |
| Setup pain | Install app, create VM | Cloud account, SSH keys, firewall rules | Medium | High |
| Speed | Shared with your Mac | Full server CPU, sim runs fast | N/A (no GUI) | N/A |
| Works from anywhere | Only on your Mac | Anywhere with internet | Only on your Mac | Only on your Mac |

**My recommendation for a beginner: start with the UTM VM.** It costs nothing, needs no accounts, and has the fewest new concepts while you are also learning ROS. Use this remote path later, when you want a faster sim, or when you want to run things while away from your Mac. Both paths run the exact same launch files.

## How the GUI problem gets solved remotely

Three options exist. This guide uses the third:

1. **XQuartz X-forwarding** (`ssh -X`): forwards the Gazebo/RViz windows to your Mac. It works, but it is laggy over the internet and needs XQuartz installed. Fine in a pinch, unpleasant daily.
2. **Headless sim + video capture**: run everything with no GUI, record video on the server. Works, but you are flying blind while developing.
3. **Foxglove (this guide)**: the sim runs headless on the server, and you watch it in Foxglove Studio on your Mac, a free web/desktop visualizer built for exactly this. No X11, no lag pain, and screen-recording the Foxglove window gives you the demo video.

## Cost

What a big-enough server costs (2 vCPU / 4 GB RAM minimum for Gazebo + Nav2):

- **Oracle Cloud Always Free: $0**, permanent free tier (4 ARM CPUs, 24 GB RAM). ARM is fine, Jazzy supports it. Caveats: account approval takes a while, and they can reclaim the machine if it sits idle for a week.
- **Hetzner CX22: ~$5 USD (~$7 CAD)/month** (2 vCPU, 4 GB). Billing is hourly capped at the monthly price, so spin it up, learn for a month, destroy it. Pick their US region for lower latency from Toronto.
- **Hetzner CX32: ~$10 USD (~$14 CAD)/month** (4 vCPU, 8 GB). Roomier, worth it if the sim feels slow.
- **DigitalOcean 2 vCPU / 4 GB: $20-24 USD (~$28-34 CAD)/month.** Polished, and they have a Toronto datacenter, but you pay for it.

Destroy the server when you are done learning and the billing stops. Do not leave it running between phases unless you are paying for the month anyway.

## Steps

### Phase 0: Create the server

- [ ] Pick a provider from the list above and create an account
- [ ] On your Mac, check for an SSH key: `ls ~/.ssh/id_ed25519.pub`
- [ ] If that file is missing, make one: `ssh-keygen -t ed25519` (press Enter three times)
- [ ] Show your public key: `cat ~/.ssh/id_ed25519.pub`, copy the whole line
- [ ] Create a server: **Ubuntu 24.04**, 2 vCPU / 4 GB or better, paste your public key when asked
- [ ] Write down the server's IP address. Call it `<IP>` below.

### Phase 1: First login and install

- [ ] `ssh root@<IP>` (type `yes` the first time it asks)
- [ ] You are now on the server. Everything below runs here until said otherwise.
- [ ] `sudo apt update && sudo apt upgrade -y`
- [ ] `sudo apt install -y git`
- [ ] `git clone https://github.com/imtisaalm/ros2-nav2-sim.git && cd ros2-nav2-sim`
- [ ] `bash scripts/install-jazzy.sh` (20-40 minutes)
- [ ] Install the two remote extras: `sudo apt install -y xvfb ros-jazzy-foxglove-bridge`
- [ ] Verify the bridge installed: `ros2 pkg list | grep foxglove` → you see `foxglove_bridge`
- [ ] Open the Foxglove port: `sudo ufw allow OpenSSH && sudo ufw allow 8765/tcp && sudo ufw enable` (type `y`)
- [ ] Close the terminal, SSH back in, then: `echo $ROS_DISTRO` → `jazzy`, `echo $TURTLEBOT3_MODEL` → `burger`

### Phase 2: See the robot (Foxglove)

- [ ] On the server, build the workspace: `cd ~/ros2-nav2-sim/ros2_ws && colcon build --symlink-install && source install/setup.bash`
- [ ] Launch the sim headless (the Gazebo window renders into a virtual display nobody watches): `xvfb-run -a ros2 launch nav2_sim_demo sim.launch.py`
- [ ] Leave that running. Open a **second** SSH session.
- [ ] In session 2: `source /opt/ros/jazzy/setup.bash && ros2 run foxglove_bridge foxglove_bridge`
- [ ] On your **Mac**, download the free Foxglove Studio desktop app from foxglove.dev and open it. (Use the desktop app, not the website: browsers block the unencrypted connection this needs.)
- [ ] In Foxglove: **Open connection** → enter `ws://<IP>:8765` → Connect
- [ ] Add a **3D** panel. In it, add the `/map` topic (as Map), the `/scan` topic, and confirm the robot model appears.
- [ ] You see the TurtleBot3 in its world. The sim is running on the server, the picture is on your Mac.

### Phase 3: Drive it

- [ ] Third SSH session: `source /opt/ros/jazzy/setup.bash && source ~/ros2-nav2-sim/ros2_ws/install/setup.bash`
- [ ] `ros2 run turtlebot3_teleop teleop_keyboard`
- [ ] Press `i` → watch the robot move in Foxglove (small delay is normal, that is internet latency)
- [ ] `k` stops it. Drive for 2 minutes.

### Phase 4: Map it

Same as the local checklist, with Foxglove as your eyes:

- [ ] New SSH session: `ros2 launch nav2_sim_demo mapping.launch.py` (source both setup lines first, every session)
- [ ] In Foxglove's 3D panel, the `/map` topic now fills in as you drive
- [ ] Drive slowly around the whole world from the teleop session until the map looks complete
- [ ] Save it: `ros2 run nav2_map_server map_saver_cli -f ~/ros2-nav2-sim/ros2_ws/src/nav2_sim_demo/maps/tb3_world`
- [ ] `ls ~/ros2-nav2-sim/ros2_ws/src/nav2_sim_demo/maps/` → `tb3_world.pgm` and `tb3_world.yaml` exist
- [ ] Ctrl+C the mapping and sim sessions

### Phase 5: Send it on missions

- [ ] SSH session: `xvfb-run -a ros2 launch nav2_sim_demo sim.launch.py`
- [ ] Another session: `ros2 launch nav2_sim_demo nav2.launch.py`
- [ ] In Foxglove, add a **Publish** panel. Set it to publish `geometry_msgs/PoseWithCovarianceStamped` on `/initialpose`: click a starting point to set the initial pose, roughly where the robot spawns.
- [ ] Wait ~20 seconds for localization to settle (the robot model snaps to the right place)
- [ ] In the Publish panel, publish `geometry_msgs/PoseStamped` on `/goal_pose`: click a target point. The robot plans and drives there.
- [ ] Send a second goal. Then a third.

RViz users get click-drag goal tools; in Foxglove it is a form you fill in. Clunkier, but it works, and everything else is identical.

### Phase 6: Show it and clean up

- [ ] Screen-record the Foxglove window on your Mac (Cmd+Shift+5): sim view, mapping timelapse, two Nav2 goals
- [ ] Fill in `docs/writeup-template.md`
- [ ] **Destroy the server** in your provider's dashboard when done, so billing stops. Your repo, writeup, and video all live outside the server, so nothing is lost.

## Latency, honestly

- Typing commands over SSH: 20-80 ms to a US region. You will not notice it.
- Teleop driving: slight delay between keypress and motion. Fine for mapping, slightly annoying for precise driving.
- Foxglove visualization: smooth on a decent connection. If it stutters, your internet is the bottleneck, not the server.
- The sim itself runs at full server speed regardless of your connection.

## Troubleshooting

**Foxglove will not connect.** The usual cause is the firewall. On the server: `sudo ufw status` should list `8765/tcp ALLOW`. Also check your provider's own firewall panel allows it.

**`xvfb-run` not found.** `sudo apt install -y xvfb`, then retry.

**Foxglove shows no robot model.** The 3D panel needs the `/robot_description` topic, which the sim publishes. If the panel is empty, the sim launch is still starting up; wait a minute.

**SSH asks for a password instead of using your key.** The key was not attached to the server. Easiest fix: destroy and recreate the server, pasting the key carefully this time.

**Everything works but feels slow.** Upgrade to the 4 vCPU / 8 GB plan, or accept it: Gazebo on shared cloud CPUs is usable, not fast.
