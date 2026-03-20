
ros2 launch ybcar_one bringup.launch.py use_sim_time:=false

ros2 launch slam_toolbox online_async_launch.py slam_params_file:=src/ybcar_one/config/mapper_params_online_async.yaml use_sim_time:=false

ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -p use_sim_time:=false