import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    
    tb3_0_config = os.path.join(get_package_share_directory('autobot'), 'config', 'amr_1_amcl_config.yaml')
    tb3_1_config = os.path.join(get_package_share_directory('autobot'), 'config', 'amr_2_amcl_config.yaml')

    map_file = os.path.join(get_package_share_directory('autobot'), 'config', 'new_warehouse_save.yaml')

    # map_file = "/home/tarun_56/pc_ws/new_warehouse_save.yaml"

    return LaunchDescription([
        Node(
            package='nav2_map_server',
            executable='map_server',
            name='map_server',
            output='screen',
            parameters=[{'use_sim_time': True}, 
                        {'topic_name':"map"},
                        {'frame_id':"map"},
                        {'yaml_filename':map_file}]
        ),
            
        Node(
            namespace='amr_1',
            package='nav2_amcl',
            executable='amcl',
            name='amcl',
            output='screen',
            parameters=[tb3_0_config]
        ),

        # Node(
        #      namespace='amr_2',
        #      package='nav2_amcl',
        #      executable='amcl',
        #      name='amcl',
        #      output='screen',
        #      parameters=[tb3_1_config]
        # ),

        Node(
            package='nav2_lifecycle_manager',
            executable='lifecycle_manager',
            name='lifecycle_manager_localization',
            output='screen',
            parameters=[{'use_sim_time': True},
                        {'autostart': True},
                        {'bond_timeout':0.0},
                        {'node_names': ['map_server', 'amr_1/amcl']}
                        ]
        )
    ])