## SLAM
ros2 launch ybcar_one bringup.launch.py use_sim_time:=false

ros2 launch slam_toolbox online_async_launch.py slam_params_file:=src/ybcar_one/config/mapper_params_online_async.yaml use_sim_time:=false

rviz2 --ros-args -p use_sim_time:=false

ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -p use_sim_time:=false


## NAV2
ros2 launch nav2_bringup bringup_launch.py use_sim_time:=false autostart:=true map:=/home/yoonki/ros/ybcar_ws/my_map.yaml

==========

ros2 launch ybcar_one bringup.launch.py use_sim_time:=false

ros2 launch slam_toolbox online_async_launch.py slam_params_file:=src/ybcar_one/config/mapper_params_online_async.yaml use_sim_time:=false

ros2 launch nav2_bringup navigation_launch.py params_file:=src/ybcar_one/config/nav2_params.yaml use_sim_time:=false

rviz2 --ros-args -p use_sim_time:=false