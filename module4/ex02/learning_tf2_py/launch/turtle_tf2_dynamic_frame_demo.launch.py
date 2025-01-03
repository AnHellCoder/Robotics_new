import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node


def generate_launch_description():
    demo_nodes = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('learning_tf2_py'), 'launch'),
            '/turtle_tf2_demo.launch.py']),
       launch_arguments={'target_frame': 'carrot1'}.items(),
       )

    return LaunchDescription([
        demo_nodes,
        DeclareLaunchArgument(
            'radius', default_value=str('3'),
            description='radius of carrot rotation'
        ),
        DeclareLaunchArgument(
            'direction_of_rotation', default_value=str('1'),
            description='radius of carrot rotation'
        ),
        Node(
            package='learning_tf2_py',
            executable='dynamic_frame_tf2_broadcaster',
            name='dynamic_broadcaster',
            parameters=[
                {'radius': LaunchConfiguration('radius'),
                'direction_of_rotation': LaunchConfiguration('direction_of_rotation')}
            ]
        ),
    ])