# Setup: Path D (Docker, fallback only)

**Read this first:** on Apple Silicon Macs, documented reports show the Gazebo and RViz GUIs fail inside Docker (no GPU passthrough, broken X11/Qt). The ROS nodes run but you cannot see anything. For a first project centered on watching a robot, that is a dealbreaker. This path stays here for Linux hosts and for headless use. Mac users: use Path A (UTM VM) or Path B (remote SSH).

## Honest notes about this path

- **On a Linux host**, this path works well. GUI apps (Gazebo, RViz) display through X11 with one extra command.
- **On a Mac**, the Gazebo GUI is the painful part. macOS has no X11 server built in, so you install XQuartz, and 3D rendering over that link is slow. It still works, it just stutters. RViz is lighter and behaves better. If you have any way to run native Ubuntu 24.04 (Path A), take it.
- **On Windows**, use WSL2 with Ubuntu 24.04, then follow Path A inside WSL2. That beats Docker Desktop for this workload.

## What you need

- Docker Desktop (or Docker Engine on Linux), 8 GB RAM for the container, 20 GB free disk.

## Build and run

From the repo root:

```bash
docker compose -f docker/docker-compose.yml build
```

Then allow GUI windows (Linux host with X11):

```bash
xhost +local:
```

Then start the container:

```bash
docker compose -f docker/docker-compose.yml up -d
docker compose -f docker/docker-compose.yml exec ros2 bash
```

Inside the container, ROS 2 is already on the path. Then follow `docs/checklist.md` from Phase 1, running all commands **inside the container**. The workspace lives at `/root/ros2_ws` inside the container and is mounted from `./ros2_ws` on your host, so files you save persist.

## Mac GUI setup (only if you need the Gazebo window)

1. Install XQuartz, log out and back in.
2. In XQuartz settings, enable "Allow connections from network clients".
3. On the Mac terminal: `xhost + $(hostname)` (or use `socat` bridging if that fails).
4. Set `DISPLAY` to your Mac's IP in the compose environment.

Expect the 3D view to be sluggish. The sim itself still runs correctly. Many people do mapping and Nav2 with RViz only on this path and skip the Gazebo window after the first look.

## Stopping

```bash
docker compose -f docker/docker-compose.yml down
```

Your workspace files stay on the host in `./ros2_ws`. Nothing is lost.

## Troubleshooting

**`cannot open display`.** The `xhost` step was skipped, or `DISPLAY` is wrong. On Linux, `echo $DISPLAY` should print something like `:0` or `:1`.

**Container eats all RAM.** Give Docker Desktop at least 8 GB in its settings. Gazebo plus Nav2 is the heaviest combo here.

**Keyboard teleop feels laggy in the container.** Normal on Mac. The keys still work; the display lags behind.
