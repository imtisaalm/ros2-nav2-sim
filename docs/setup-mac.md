# Setup: Mac (primary path)

Your Mac cannot run ROS 2 Jazzy natively in any beginner-friendly way, so we give it a Linux computer inside your Mac: a free Ubuntu 24.04 virtual machine using UTM. Inside that VM, everything installs with `apt` exactly like the standard tutorials. This is the path I recommend.

## Why this path and not the others

- **UTM + Ubuntu VM (this guide):** free, and inside the VM you are on a fully supported platform (ROS 2 Jazzy officially supports Ubuntu 24.04 on ARM64). Every install command just works. Downside: the 3D Gazebo view is CPU-rendered and slow. RViz, where you do the real work, runs fine.
- **Remote Linux over SSH:** rent a small cloud server (~$5-10 USD/month, $0 possible), run everything there, watch it in Foxglove on your Mac. Full-speed sim, works from anywhere, but adds cloud accounts, SSH keys, and firewall rules on top of learning ROS. Documented in `docs/setup-remote.md`. My pick for later, not for project one.
- **Docker:** not recommended on Apple Silicon. Documented reports show the Gazebo and RViz GUIs fail on Apple Silicon Macs (no GPU passthrough, broken X11/Qt). The ROS nodes run, but you cannot see anything, which defeats the purpose for a first project.
- **RoboStack / native macOS:** not recommended. It needs conda-based ROS plus Homebrew Gazebo, and the ROS-Gazebo bridge has a known protobuf incompatibility on macOS that breaks the exact piece TurtleBot3 simulation needs. It also involves source builds and Xcode workarounds. Maybe later, not for project one.

## What you need

- Your Mac, with 20 GB free disk and ideally 16 GB RAM (8 GB works, the VM gets half)
- About an hour for VM setup, most of it waiting on downloads

## Steps

### 1. Install UTM

- [ ] Download UTM from mac.getutm.app (it is free and open source)
- [ ] Open the downloaded file and drag UTM into Applications

### 2. Create the Ubuntu VM

- [ ] Open UTM, click **Create a New Virtual Machine**
- [ ] Choose **Virtualize** (not Emulate, that is much slower)
- [ ] Choose **Linux**
- [ ] For the boot ISO: UTM offers to download Ubuntu for you in its gallery. Take that option if offered and pick **Ubuntu 24.04**.
- [ ] If it does not offer: download the **ARM64** Ubuntu 24.04 desktop ISO from ubuntu.com yourself, then point UTM at the file. (Intel Mac: use the regular 64-bit Intel ISO instead. Everything after this point is identical.)
- [ ] Give the VM **8 GB RAM** (or at least 4 GB), **4 CPU cores**, and a **40 GB** drive
- [ ] Finish the wizard, start the VM, and install Ubuntu normally (pick your name, password, all defaults)
- [ ] When Ubuntu is installed, open a terminal inside the VM and update it: `sudo apt update && sudo apt upgrade -y`

### 3. Install ROS 2 inside the VM

- [ ] Inside the VM, clone this repo: `git clone https://github.com/imtisaalm/ros2-nav2-sim.git` (install git first if needed: `sudo apt install -y git`)
- [ ] `cd ros2-nav2-sim`
- [ ] `bash scripts/install-jazzy.sh` (20-40 minutes, mostly downloading)
- [ ] Close the VM terminal, open a new one
- [ ] `echo $ROS_DISTRO` → expect `jazzy`
- [ ] `echo $TURTLEBOT3_MODEL` → expect `burger`

### 4. One graphics tweak (prevents Gazebo crashes in the VM)

The VM has no real GPU, so we tell Gazebo to render with the CPU and not try anything fancy:

- [ ] Run: `echo 'export LIBGL_ALWAYS_SOFTWARE=1' >> ~/.bashrc`
- [ ] Close the terminal, open a new one

### 5. Continue with the checklist

- [ ] Open `docs/checklist.md` and start at Phase 1. Everything from here runs inside the VM.

## What to expect on screen

- **RViz** (the window where you watch the map and send goals): works fine, this is your main window.
- **Gazebo** (the 3D world view): opens and runs, but the 3D rendering is slow and choppy. That is normal in a VM. The simulation itself (physics, laser scans, the robot driving) runs correctly underneath. If the 3D view bothers you, minimize it and work in RViz.
- **Screen recording:** record the UTM window from macOS with Cmd+Shift+5. See `docs/screen-capture.md`.

## Troubleshooting

**The VM feels sluggish overall.** Give it more RAM/CPU in UTM settings (shut the VM down first). Close heavy Mac apps while running the sim.

**Gazebo crashes on launch.** Make sure the `LIBGL_ALWAYS_SOFTWARE=1` line is in `~/.bashrc` and you opened a new terminal after adding it.

**`ros2` commands say "command not found" inside the VM.** The install script did not finish, or you skipped the close-and-reopen-terminal step. Re-run `bash scripts/install-jazzy.sh`; it is safe to re-run.

**Copy-paste between Mac and VM is awkward.** It is. For commands, type them or use a shared note. For files, `git` is the bridge: commit on one side, pull on the other.
