#!/usr/bin/env python3

import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.actions import OpaqueFunction
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import Command
from launch.actions import TimerAction

def launch_setup(context, *args, **kwargs):

    x_spawn = LaunchConfiguration('x_spawn').perform(context)
    y_spawn = LaunchConfiguration('y_spawn').perform(context)
    entity_name = LaunchConfiguration('entity_name').perform(context)

    print("###############################################################")
    print("SPAWN MULTI Robot="+str(entity_name)+",["+str(x_spawn)+","+str(y_spawn)+"]")
    print("###############################################################")


    # ROBOT STATE PUBLISHER
    ####### DATA INPUT ##########

    use_ros2_control = LaunchConfiguration('use_ros2_control')

    xacro_file = 'robot.urdf.xacro'

    
    package_description = "autobot"
    robot_desc_path = os.path.join(get_package_share_directory(package_description), "description", xacro_file)
    # robot_description_config = Command(['xacro ', xacro_file, ' use_ros2_control:=', use_ros2_control, ' sim_mode:=', use_sim_time])
    
    robot_state_publisher_node = Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            namespace=entity_name,
        parameters=[{'frame_prefix': entity_name+'/', 'use_sim_time': True, 'robot_description': Command(['xacro ', robot_desc_path, ' robot_name:=', entity_name])}],
        output="screen"
    )

    joint_state_publisher_node = Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            name='joint_state_publisher',
            namespace=entity_name,
        parameters=[{'frame_prefix': entity_name+'/', 'use_sim_time': True, 'robot_description': Command(['xacro ', robot_desc_path, ' robot_name:=', entity_name])}],
        output="screen"
    )
    # Spawn ROBOT Set Gazebo
    start_gazebo_ros_spawner_cmd = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        name='spawn_entity',
        namespace=entity_name,
        output='screen',
        arguments=['-entity',
                   entity_name,
                   '-x', x_spawn, '-y', y_spawn,
                   '-topic', 'robot_description',
                   '-timeout', '120.0'
                   ]
    )

    twist_mux_params = os.path.join(get_package_share_directory(package_description), 'config', 'twist_mux.yaml')
    twist_mux = Node(
        package="twist_mux",
        executable="twist_mux",
        parameters=[twist_mux_params, {'use_sim_time': True}],
        remappings=[(f'/{entity_name}/cmd_vel_out', f'/{entity_name}/diff_cont/cmd_vel_unstamped')]
    )



    return [robot_state_publisher_node, joint_state_publisher_node, start_gazebo_ros_spawner_cmd, twist_mux]


def generate_launch_description(): 

    x_spawn_arg = DeclareLaunchArgument('x_spawn', default_value='-7.18')
    y_spawn_arg = DeclareLaunchArgument('y_spawn', default_value='-0.13')
    entity_name_arg = DeclareLaunchArgument('entity_name', default_value='amr_1')
    

    return LaunchDescription([
        x_spawn_arg,
        y_spawn_arg, 
        entity_name_arg,
        OpaqueFunction(function = launch_setup)
        ])