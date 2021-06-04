FROM ros:foxy
# Setup all the keys and install packages which need root access.
USER root
RUN . /opt/ros/foxy/setup.sh && \
    apt-get update && \
    apt-get install -y wget gnupg2 lsb-release && \
    apt-get install -y python3-colcon-common-extensions && \
    sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable `lsb_release -cs` main" > /etc/apt/sources.list.d/gazebo-stable.list' && \
    wget http://packages.osrfoundation.org/gazebo.key -O - | sudo apt-key add - && \
    apt-get update && \
    apt-get install -y ignition-citadel
# Setup artpark user.
# RUN groupadd -g 1000 artpark && \
#     useradd -d /home/artpark -s /bin/bash -m artpark -u 1000 -g 1000
# Clone all the necessary sources and install deps through rosdep.
RUN wget https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc -O - | sudo apt-key add - && \
    sh -c 'echo "deb [arch=$(dpkg --print-architecture)] http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" > /etc/apt/sources.list.d/ros2-latest.list' && \
#  From Install development tools and ROS tools section at https://docs.ros.org/en/foxy/Installation/Ubuntu-Development-Setup.html#install-dependencies-using-rosdep 
sudo apt update && sudo apt install -y \   
  build-essential \
  cmake \
  git \
  libbullet-dev \
  python3-colcon-common-extensions \
  python3-flake8 \
  python3-pip \
  python3-pytest-cov \
  python3-rosdep \
  python3-setuptools \
  python3-vcstool \
  wget &&\
python3 -m pip install -U \
  argcomplete \
  flake8-blind-except \
  flake8-builtins \
  flake8-class-newline \
  flake8-comprehensions \
  flake8-deprecated \
  flake8-docstrings \
  flake8-import-order \
  flake8-quotes \
  pytest-repeat \
  pytest-rerunfailures \
  pytest &&\
sudo apt install --no-install-recommends -y \
  libasio-dev \
  libtinyxml2-dev &&\
sudo apt install --no-install-recommends -y \
  libcunit1-dev