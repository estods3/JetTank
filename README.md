# JetTank
An adaptation of Jetbot built on NVIDIA Jetson Nano.

## Description
A set of sample programs and a ROS-based software architecture used to demonstrate ROS-based controls and debugging.

<img src="https://github.com/estods3/JetTank/blob/master/documentation/JetTankBuild.jpg" alt="drawing" width="300"/><img src="https://github.com/estods3/JetTank/blob/master/documentation/nodegraph.png" alt="drawing" width="300"/>
              picture of JetTank    screenshot of node  graph


## Differences from Official NVIDIA Jetbot
There are some minor hardware differences between this implementation of NVIDIA's official Jetbot, however, the ROS-based software architecture and algorithms used in this repository could be modified to work for the official version. The major differences are listed below:

1. Uses a homemade motor driver breakout board using an H bridge IC.
Using an H bridge motor controller means that the Jetson Nano is tied to a positive and negative GPIO pin for each motor. Setting one pin as HIGH and the other as LOW means the motor will spin (reversing the pins will spin the motor the other direction). This made controlling the robot different from the official Jetbot, however, the library files in "lib" provide the function calls to maneuver the robot in any desired direction.

2. Uses an off-the-shelf Logitec USB camera (Interfaced using OpenCV).

## Setup
Hardware and software setup.

### Hardware
A hardware installation is provided by NVIDIA on their official Jetbot wiki (https://github.com/NVIDIA-AI-IOT/jetbot/wiki).
This can be used to complete the build needed to run the programs in this repository.

Minor design differences were implemented based on parts available. These are described in the previous section.

### Software
This repository contains Robotic Operating System (ROS) packages for a "JetTank" robot and a "Command Center" host PC.
Installation guidelines are provided in each package README.md.

This repository contains a "How to Run" README.md in "src".

NOTE: it is worth following the official Jetbot wiki (https://github.com/NVIDIA-AI-IOT/jetbot/wiki) to install dependencies such as deep learning modules, OpenCV, and the Jetson GPIO package. Although this wiki contains instructions for installing more packages than are used for this project, it is worth installing them for future use.

## Jetson Programs
Below are the programs included in this repository.

### 1. Line Following

This program will perform the classic line following exercise where the robot will use the camera to identify a line and follow it.

![jetTank](https://github.com/estods3/JetTank/blob/master/documentation/linefollowing.gif)

### 2. Workspace

This program uses a line as a boundary of a workspace in which the robot is intended to be confined to. The robot will manuever about the workspace, stopping and turning around each time it reaches the boundary of the workspace.

![jetTank](https://github.com/estods3/JetTank/blob/master/documentation/workspace.gif)

### 3. Remote Control

A program to control robot remotely using a rostopic from "Command Center" on another PC.

## Command Center Debugging Environment (running on a linux PC)
A ROS-based debugging environment to view camera feed and control the program JetTank is running.

![jetTank](https://github.com/estods3/JetTank/blob/master/documentation/commandcenter.png)
screenshot of Command Center GUI and Video Feed

### GUI
A GUI can be used to select between programs that are being run. The "Remote Control" button will allow the user to use the up, down, right, and left arrows on the host computer to control the robot remotely. The "STOP" button will immediately halt the robot.

### Video Feed
A video feed provides real-time video from the robot. The size and color of this feed can be adjusted based on the strength of the wifi signal.
