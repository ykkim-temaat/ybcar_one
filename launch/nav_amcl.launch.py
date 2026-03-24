import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, GroupAction, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import SetRemap

def generate_launch_description():
    # 1. 패키지 경로 설정
    # ROS 2 시스템이 설치된 디렉토리에서 패키지 위치를 자동으로 찾습니다.
    ybcar_one_dir = get_package_share_directory('ybcar_one')
    nav2_bringup_dir = get_package_share_directory('nav2_bringup')

    # 2. Launch Configuration 변수 (터미널에서 인자로 받을 수 있도록 셋팅)
    use_sim_time = LaunchConfiguration('use_sim_time')
    autostart = LaunchConfiguration('autostart')
    map_yaml_file = LaunchConfiguration('map')
    params_file = LaunchConfiguration('params_file')

    # 3. 파일 기본 경로 하드코딩 (터미널에서 안 적어주면 이 경로를 씁니다)
    # 회원님의 맵 절대 경로
    default_map_path = '/home/yoonki/ros/ybcar_ws/my_map4.yaml' 
    # 회원님의 파라미터 파일 경로 (install 폴더 기준)
    default_params_path = os.path.join(ybcar_one_dir, 'config', 'nav2_params.yaml')

    # 4. Launch Argument 선언 (기본값 부여)
    declare_use_sim_time = DeclareLaunchArgument(
        'use_sim_time', default_value='false', description='Use sim time if true'
    )
    declare_autostart = DeclareLaunchArgument(
        'autostart', default_value='true', description='Automatically startup the nav2 stack'
    )
    declare_map_yaml = DeclareLaunchArgument(
        'map', default_value=default_map_path, description='Full path to map yaml file to load'
    )
    declare_params_file = DeclareLaunchArgument(
        'params_file', default_value=default_params_path, description='Full path to the ROS 2 parameters file to use'
    )

    # 5. Nav2 실행 및 리매핑 (가장 중요한 부분!)
    # GroupAction으로 묶어서, 이 안에서 실행되는 모든 노드의 /cmd_vel 출력을 /cmd_vel_nav로 강제 리매핑합니다.
    nav2_group = GroupAction([
        SetRemap(src='/cmd_vel', dst='/cmd_vel_nav'),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(nav2_bringup_dir, 'launch', 'bringup_launch.py')),
            launch_arguments={
                'use_sim_time': use_sim_time,
                'autostart': autostart,
                'map': map_yaml_file,
                'params_file': params_file
            }.items()
        )
    ])

    # 6. 최종 LaunchDescription 반환
    return LaunchDescription([
        declare_use_sim_time,
        declare_autostart,
        declare_map_yaml,
        declare_params_file,
        nav2_group
    ])