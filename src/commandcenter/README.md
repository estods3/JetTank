# ROS Package: commandcenter
description: package containing visualization and GUI ROS nodes and setup scripts needed to install and monitor program execution on a jetson nano Jetbot.
This package is compatible with the "jettank" package.

## Installation
Some nodes in this package run Python2 while others run Python3. A roslaunch script is included in this package to launch the correct nodes using the proper Python version.
However, certain packages need to be installed to different version of Python. The packages needed can be found in the files below.

requirements2.txt - for Python2. NOTE: ROS and OpenCV will likely need to be built from scratch. There are many tutorials online outlining how to install these packages.

requirements3.txt - for Python3. NOTE: ROS will likely need to be built from scratch. There are many tutorials online outlining how to install these packages.
