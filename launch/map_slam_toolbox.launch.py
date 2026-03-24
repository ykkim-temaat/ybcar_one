import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    # 1. 패키지 경로 탐색
    ybcar_one_dir = get_package_share_directory('ybcar_one')
    slam_toolbox_dir = get_package_share_directory('slam_toolbox')

    # 2. Launch Configuration 변수 설정
    use_sim_time = LaunchConfiguration('use_sim_time')
    slam_params_file = LaunchConfiguration('slam_params_file')

    # 3. Launch Argument 선언 (기본값 내장)
    declare_use_sim_time = DeclareLaunchArgument(
        'use_sim_time', default_value='false', description='Use sim time if true'
    )
    declare_slam_params_file = DeclareLaunchArgument(
        'slam_params_file',
        default_value=os.path.join(ybcar_one_dir, 'config', 'mapper_params_online_async.yaml'),
        description='Full path to the ROS2 parameters file to use for the slam_toolbox node'
    )

    # 4. SLAM Toolbox 실행
    slam_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(slam_toolbox_dir, 'launch', 'online_async_launch.py')),
        launch_arguments={
            'use_sim_time': use_sim_time,
            'slam_params_file': slam_params_file
        }.items()
    )

    # 5. RViz2 실행 (맵핑 중에는 실시간 모니터링이 필수이므로 같이 켭니다)
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time}],
        # 만약 맵핑 전용으로 저장해둔 RViz 설정 파일(.rviz)이 있다면 아래 주석을 풀고 경로를 지정하세요!
        # arguments=['-d', os.path.join(ybcar_one_dir, 'rviz', 'mapping_view.rviz')]
    )

    # 6. 반환
    return LaunchDescription([
        declare_use_sim_time,
        declare_slam_params_file,
        slam_launch,
        rviz_node
    ])