# JetTank
An adaptation of Jetbot built on NVIDIA Jetson Nano.

## Description

![jetTank](https://github.com/estods3/JetTank/blob/master/documentation/JetTankBuild.jpg)
picture of JetTank

### Differences from Official NVIDIA Jetbot
1. Uses a homemade motor driver breakout board using an H bridge IC.
Using an H bridge motor controller means that the Jetson Nano is tied to a positive and negative GPIO pin for each motor. Setting one pin as HIGH and the other as LOW means the motor will spin (reversing the pins will spin the motor the other direction). This made controlling the robot different from the official Jetbot, however, the library files in "lib" provide the function calls to maneuver the robot in any desired direction.

2. Uses an off-the-shelf Logitec USB camera.

## Setup
Hardware and software setup.

### Hardware


### Software

#### ROS

1. list IP and hostnames of the JetTank and host PC used to operate the debugging interface in:

```/etc/hosts```

on both the JetTank file and host PC file.

2. On JetTank, edit the ~/.bashrc file to point to the ROS_MASTER_URI of the JetTank:

```export ROS_MASTER_URI=http://jetson-nano:11311
export ROS_HOSTNAME=jetson-nano
export ROS_IP=jetson-nano
```

3. On host PC, edit the ~/.bashrc file to point to the ROS_MASTER_URI of the JetTank as shown below:

```export ROS_MASTER_URI=http://jetson-nano:11311
export ROS_HOSTNAME=optiplexPC
export ROS_IP=optiplexPC
```
4. Start ROS on the JetTank by opening an ssh terminal and typing:

```source ~/.bashrc```

followed by:

```roscore```

5. To start using the JetTank, open another SSH terminal and type:

```source ~/.bashrc```

and execute any of the programs described below.

#### Dependencies

1. ROS

2. OpenCV

## Programs
Below are the programs included in this repository. All programs are intended to be run with Python3

### 1. Line Following

This program will perform the classic line following exercise where the robot will use the camera to identify a line and follow it.

![jetTank](https://github.com/estods3/JetTank/blob/master/documentation/linefollowing.gif)



### 2. Workspace

This program uses a line as a boundary of a workspace in which the robot is intended to be confined to. The robot will manuever about the workspace, stopping and turning around each time it reaches the boundary of the workspace.

![jetTank](https://github.com/estods3/JetTank/blob/master/documentation/workspace.gif)


### 3. Remote Control

A program to control robot remotely using a rostopic from "Command Center" on another PC.

## Command Center Debugging Environment
A ROS-based debugging environment to view camera feed and control the program JetTank is running.
