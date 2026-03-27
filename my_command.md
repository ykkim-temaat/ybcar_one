## 1. SLAM (mapping)
``` bash
ros2 launch ybcar_one bringup.launch.py use_sim_time:=false
ros2 launch slam_toolbox online_async_launch.py slam_params_file:=src/ybcar_one/config/mapper_params_online_async_mapping.yaml use_sim_time:=false
rviz2 --ros-args -p use_sim_time:=false
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -p use_sim_time:=false -r /cmd_vel:=/cmd_vel_keyboard
```
### launch file
``` bash
ros2 launch ybcar_one bringup.launch.py use_sim_time:=false
ros2 launch ybcar_one map_slam_toolbox.launch.py use_sim_time:=false
```

## 2. NAV2 with nav2_amcl (localization_launch.py)
``` bash
ros2 launch ybcar_one bringup.launch.py use_sim_time:=false
ros2 launch nav2_bringup bringup_launch.py use_sim_time:=false autostart:=true map:=/home/yoonki/ros/ybcar_ws/my_map2.yaml params_file:=src/ybcar_one/config/nav2_params.yaml
rviz2 --ros-args -p use_sim_time:=false
```

### launch file
``` bash
ros2 launch ybcar_one bringup.launch.py use_sim_time:=false
ros2 launch ybcar_one nav_amcl.launch.py use_sim_time:=false
rviz2 --ros-args -p use_sim_time:=false
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -p use_sim_time:=false -r /cmd_vel:=/cmd_vel_keyboard
```

## 3. NAV2 with with slam_toolbox (slam_launch.py)
``` bash
ros2 launch ybcar_one bringup.launch.py use_sim_time:=false
ros2 launch slam_toolbox online_async_launch.py slam_params_file:=src/ybcar_one/config/mapper_params_online_async.yaml use_sim_time:=false
ros2 launch nav2_bringup navigation_launch.py params_file:=src/ybcar_one/config/nav2_params.yaml use_sim_time:=false 
rviz2 --ros-args -p use_sim_time:=false
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -p use_sim_time:=false -r /cmd_vel:=/cmd_vel_keyboard
```

### launch file
``` bash
ros2 launch ybcar_one bringup.launch.py use_sim_time:=false
ros2 launch ybcar_one nav_slam_toolbox.launch.py use_sim_time:=false
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -p use_sim_time:=false -r /cmd_vel:=/cmd_vel_keyboard
```


