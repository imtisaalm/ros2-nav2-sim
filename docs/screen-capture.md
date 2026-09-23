# Screen capture: recording the demo video

The demo video is the portfolio artifact. Keep it short: 2 minutes beats 10.

## Easiest option: SimpleScreenRecorder (Ubuntu)

```bash
sudo apt install simplescreenrecorder
```

Open it, select "Record a fixed rectangle", drag over the RViz window, hit record. 30 fps, default quality is plenty.

## macOS / Windows

Use the built-in screen recorder (Cmd+Shift+5 on Mac, Xbox Game Bar on Windows). Docker path users: record the host screen, the container windows are just windows.

## Phone fallback

If screen recording fights you, prop your phone up and film the monitor. Slightly scrappy is fine. A real recording beats a perfect plan you never execute.

## What to record (in order)

1. **10 seconds:** Gazebo window, robot sitting in the world. (Proves the sim runs.)
2. **20 seconds:** RViz during mapping, map filling in as you drive. (Proves SLAM works.)
3. **60-90 seconds:** RViz during Nav2. Set the 2D pose estimate, then click 2-3 nav goals. Let the viewer watch the green plan line and the robot driving it. (Proves autonomy.)
4. **Optional 10 seconds:** the saved `tb3_world.pgm` map image open in an image viewer.

No narration needed. Add a title card at the start with the project name if you like. Upload wherever you keep videos, link it from the writeup.
