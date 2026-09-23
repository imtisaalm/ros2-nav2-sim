# Project writeup

Copy this into a new file, fill it in, and link your demo video. Plain language. Write it like you are telling a friend what you did.

---

## What I built

(2-3 sentences. Example: "A simulated TurtleBot3 that maps its world with SLAM and drives to goals I click, using ROS 2 Jazzy, Gazebo Harmonic, and Nav2.")

Demo video: [link]

## Why this project

(Why ROS 2? What role does it play in the robotics jobs you want?)

## How it works

- **Simulation:** Gazebo Harmonic runs the physics and the TurtleBot3 model.
- **Mapping:** SLAM Toolbox turns LiDAR scans into a 2D occupancy grid while I drive.
- **Autonomy:** Nav2 takes the saved map, localizes with AMCL, plans with NavFn, and drives with the DWB controller to each goal I click in RViz.

(Keep each bullet to one line. If you can explain it simply, you understand it.)

## What I learned

- (Something about ROS 2 topics, nodes, or launch files)
- (Something about SLAM: what the map actually is)
- (Something about Nav2: what localization vs planning vs control means)

## What was hard

(Be honest. The hard parts are the interesting parts to employers.)

## What is next

(One sentence. Example: "Next I want to try the same Nav2 stack on a physical robot" or "Next: benchmark policy inference latency against this stack.")
