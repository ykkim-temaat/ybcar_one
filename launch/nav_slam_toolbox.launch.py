import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, GroupAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node, SetRemap

def generate_launch_description():
    pkg_name = 'ybcar_one'
    pkg_path = get_package_share_directory(pkg_name)

    use_sim_time = LaunchConfiguration('use_sim_time')

    # 설정 파일 경로
    slam_params = os.path.join(pkg_path, 'config', 'mapper_params_online_async.yaml')
    nav2_params = os.path.join(pkg_path, 'config', 'nav2_params.yaml')

    # 1. SLAM Toolbox 실행
    slam_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('slam_toolbox'), 'launch', 'online_async_launch.py')]),
        launch_arguments={'use_sim_time': use_sim_time, 'slam_params_file': slam_params}.items()
    )

    # 2. Nav2 자율주행 실행 (리매핑 마법 적용)
    # GroupAction으로 묶어서 이 그룹 안에서만 /cmd_vel이 /cmd_vel_nav로 바뀌도록 격리합니다.
    nav2_group = GroupAction([
        SetRemap(src='/cmd_vel', dst='/cmd_vel_nav'),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([os.path.join(
                get_package_share_directory('nav2_bringup'), 'launch', 'navigation_launch.py')]),
            launch_arguments={'use_sim_time': use_sim_time, 'params_file': nav2_params}.items()
        )
    ])

    # 3. RViz2 실행
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time}],
        # arguments=['-d', rviz_config_path] # 나중에 rviz 설정 파일(.rviz)을 만드시면 주석을 풀고 경로를 연결하세요!
    )

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='false', description='Use sim time'),
        slam_launch,
        nav2_group,
        rviz_node
    ])