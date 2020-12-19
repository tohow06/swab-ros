# swab-ros

ros package for swabbing machine


## Installation

- Clone the package into the source directory . 

        cd ~/ros-workspace/src
        git clone https://github.com/tohow06/swab-ros.git

- Build the packages

        cd ~/ros-workspace
        catkin_make

- Add in environment

        source ~/ros-workspace/src/devel/setup.bash

## Usage

- Using xbox one controller

        roscore
        rosrun swab connect_joystick_one.py