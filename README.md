# ROS 2  Task — 2-DOF Robot Arm

> **Ubuntu**
> **ROS2 version:** ROS 2 Jazzy
> **Requirements:** Docker + Docker Compose — nothing else needed on your machine

---

## Your Task

This repo contains a skeleton ROS2 package for a 2-DOF robot arm.
**Three parts are left unimplemented**, each marked with a `TODO` comment.
Complete them. We will run our own evaluator against your submission.

---

## What to Implement

### TODO 1 — TF Publisher
**File:** `ros2_ws/src/robot_arm/robot_arm/tf_publisher.py`

Publish the following TF2 transform chain at 50 Hz:

```
world
  └── base_link        (static, identity)
        └── link1      (rotates around Z — amplitude: 45°, frequency: 0.5 Hz)
              └── link2          (static, x = 0.3 m offset)
                    └── end_effector  (static, x = 0.2 m offset)
```

---

### TODO 2 — End-Effector Pose Publisher
**File:** `ros2_ws/src/robot_arm/robot_arm/pose_publisher.py`

Look up the `world → end_effector` transform via TF2 and publish it as
`geometry_msgs/PoseStamped` on `/end_effector_pose` at **10 Hz**.

The node must handle TF exceptions gracefully — it must not crash if the
transform is temporarily unavailable.

---

### TODO 3 — Launch file

Start your nodes via a the launch file `ros2_ws/src/robot_arm/launch/robot.launch.py`.

---

### TODO 4 — Bonus (optional, ~20 min)

Not in this repo. Described below under [Bonus](#bonus).

---

## Running Your Solution

### Start the robot node

```bash
xhost +local:docker
docker compose up --build
```

---

## Repository Structure

```
.
├── docker-compose.yml
├── Dockerfile                          (complete — do not modify)
├── entrypoint.sh                       (complete — do not modify)
└── ros2_ws/
    └── src/robot_arm/
        ├── robot_arm/
        │   ├── tf_publisher.py         ← TODO 1
        │   └── pose_publisher.py       ← TODO 2
        ├── launch/robot.launch.py      ← TODO 3
        ├── urdf/robot_arm.urdf         (complete — do not modify)
        └── rviz/robot.rviz             (complete — do not modify)
```

---

## Rules

- Only modify files with `TODO` comments.
  If you change anything else, explain why in your submission note.
- `docker compose up --build` must work without any manual setup steps (xhost +local:docker).
---

## Bonus

If you have extra time, write a short Python script (outside the ROS2 package)
that subscribes to `/end_effector_pose` and verifies the joint is actually
animating — not just that messages are arriving. Think about what "animating
correctly" means and how you'd detect it programmatically.

This is the kind of check we run on your submission. Seeing how you approach it
tells us a lot.

---

## Submission

Fork this repo, complete the TODOs, and send us a link to your fork.

Include a short note (a few sentences) explaining:
1. Any design decisions that aren't obvious from reading the code.
2. How you verified your solution worked locally.
3. Anything you'd improve with more time.

## Submission Notes

I completed all required TODOs and verified the solution locally using both RViz visualization and ROS topic inspection. The robot arm moves smoothly with the expected oscillatory motion, and the end-effector pose is correctly published and updated over time.

For the TF publisher, I separated static and dynamic transforms using appropriate broadcasters and implemented the motion as a sinusoidal rotation based on time. I also made sure to follow the required frame hierarchy exactly as specified.

To verify correctness, I used:
- RViz to visually confirm the motion of the robot arm  
- `ros2 topic echo /end_effector_pose` to confirm changing values  
- an additional Python script (bonus) that programmatically checks whether the end-effector position changes over time  

With more time, I would:
- improve code structure further (e.g. clearer separation of logic and configuration)  
- add more robust validation (e.g. checking motion frequency and amplitude)  
- include unit tests or a more formal verification approach  

### Bonus

A verification script (`verify_motion.py`) is included outside the ROS2 package.
It subscribes to `/end_effector_pose` and checks if the end-effector position changes over time.