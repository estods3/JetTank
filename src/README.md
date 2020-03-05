# How to Run Programs
Clone this repository onto both an nvidia jetson and a linux PC. Then follow the instuctions below to interface the two machines over wifi using ROS.
  _____________           _____________
 |   NVIDIA    |         |    Linux    |
 |   Jetson    |-- wifi--|     PC      |
 |  (Running   |         |             |
 |   roscore)  |         |             |
 |_____________|         |_____________|
 
## Create connection between Robot and PC
Once you have installed ROS and other dependencies on the Jetson and a PC (using the README.md files in each package folder), follow the steps below.

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
export ROS_HOSTNAME=PC_HOST_NAME_HERE
export ROS_IP=PC_HOST_IP_HERE
```

## Build package, Start roscore and Nodes on Jetson
Navigate to the cloned repository on your Jetson through an SSH terminal.
then type

```catkin build```

NOTE: you may need to use "chmod" on the python and shell scripts in the cloned repository for this to work properly.

If the package builds successfully, start a roscore and the jettank nodes by running
```./runJettank.sh```

NOTE: this shell script launches a roslaunch script which will automatically start roscore if one is not already started.

## Build package, Start Nodes on Linux Computer
Navigate to the cloned repository on your computer.
then type

```catkin build```

NOTE: you may need to use "chmod" on the python and shell scripts in the cloned repository for this to work properly.

If the package builds successfully, start a roscore and the jettank nodes by running
```./runCC.sh```

NOTE: this shell script launches a roslaunch script which will automatically start roscore if one is not already started.
