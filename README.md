# JetTank
An adaptation of Jetbot built on NVIDIA Jetson Nano.

## Description

![jetTank](https://github.com/estods3/JetTank/blob/master/documentation/JetTankBuild.jpg)

### Differences from Official NVIDIA Jetbot
1. Uses a homemade motor driver breakout board using an H bridge IC.
Using an H bridge motor controller means that the Jetson Nano is tied to a positive and negative GPIO pin for each motor. Setting one pin as HIGH and the other as LOW means the motor will spin (reversing the pins will spin the motor the other direction). This made controlling the robot different from the official Jetbot, however, the library files in "lib" provide the function calls to maneuver the robot in any desired direction.

2. Uses an off-the-shelf Logitec USB camera.

## Programs

### Line Following

This program will perform the classic line following exercise where the robot will use the camera to identify a line and follow it.

![jetTank](https://github.com/estods3/JetTank/blob/master/documentation/linefollowing.gif)



### Workspace

This program uses a line as a boundary of a workspace in which the robot is intended to be confined to. The robot will manuever about the workspace, stopping and turning around each time it reaches the boundary of the workspace.

![jetTank](https://github.com/estods3/JetTank/blob/master/documentation/workspace.gif)


### Remote Control
coming soon!
