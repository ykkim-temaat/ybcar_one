import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():

    # 패키지 이름 및 경로 설정
    pkg_name = 'ybcar_one'
    pkg_path = os.path.join(get_package_share_directory(pkg_name))

    # Launch Configuration 변수 설정
    use_sim_time = LaunchConfiguration('use_sim_time')

    # 1. 외부 런치 파일(rsp.launch.py) 불러오기 (Include)
    # 중복 코드 없이 기존 런치 파일을 모듈처럼 가져다 씁니다.
    rsp_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(pkg_path, 'launch', 'rsp.launch.py')]),
        # 현재의 use_sim_time 변수값을 하위 파일(rsp.launch.py)로 전달합니다.
        launch_arguments={'use_sim_time': use_sim_time}.items()
    )

    # 2. EKF 설정 파일(ekf.yaml) 경로 지정
    ekf_config_path = os.path.join(pkg_path, 'config', 'ekf.yaml')

    # 3. EKF 노드 생성
    node_ekf = Node(
        package='robot_localization',
        executable='ekf_node',
        name='ekf_filter_node',
        output='screen',
        parameters=[ekf_config_path, {'use_sim_time': use_sim_time}],
        # 필터링된 오도메트리를 표준 이름인 /odom으로 변경하여 발행합니다.
        remappings=[('odometry/filtered', '/odom')]
    )

    # Launch!
    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use sim time if true'),

        rsp_launch, # 불러온 rsp.launch.py 실행
        node_ekf    # EKF 노드 실행
    ])