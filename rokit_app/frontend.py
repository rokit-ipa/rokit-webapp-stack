from fastapi import FastAPI
import random
from nicegui import ui
from rokit_app.rokitAPI import main as api
from rokit_app.rokitAPI.models import TestParameters, TestResults
import rokit_app.frontend_helper as frontend_helper
import shlex
import os
import signal
import asyncio 

# Define the constants
conditions_file_path = "rokit_app/static/conditions.md"
protocols_file_path = "rokit_app/static/protocols.md"
tab_list = ["Run Tests", "Results", "Test Protocols", "Test Conditions"]
test_list = ["MAX_VELOCITY", "MAX_VELOCITY_SLOPE"]
ros_launch_command = "ros2 launch vicon_calculator.launch.py"
# define some global variables
process = None
task = None
result =  TestResults()


def init(fastapi_app: FastAPI) -> None:

    def read_markdown_file(file_path):
        with open(file_path, "r") as f:
            markdown_content = f.read()
        return markdown_content

    def submit_params(payload):
        api.set_params(payload)
    
    async def wait_for_process(process):
        await process.wait()
    
    async def stop_app(): 
        print("I want to cancel, but dont do it")
        print(process)
        task.cancel()
        process.send_signal(signal.SIGINT)
    
    async def start_app(payload):
        """Run a ros_launch_command in the background and display the output in the pre-created dialog."""        
        ros_launch_command = "ros2 launch vicon_calculator.launch.py"
        ros_launch_command += f" --test_name:={payload.test_name}"
        ros_launch_command += f" --trial_number:={payload.trial_number}"
        ros_launch_command += f" --robot_name:={payload.robot_name}"
        ros_launch_command += f" --tracking_object:={payload.tracking_object}"
        ros_launch_command += f" --temperature:={payload.temperature}"
        ros_launch_command += f" --humidity:={payload.humidity}"
        ros_launch_command += f" --inclination:={payload.inclination}"
        ros_launch_command += f" --floor_type:={payload.floor_type}"
        ros_launch_command += f" --notes:={payload.notes}"
            
        print("HERE IS PARAMETER LIST")
        print(ros_launch_command)
        process = await asyncio.create_subprocess_exec(
            *shlex.split(ros_launch_command), cwd=os.path.dirname(os.path.abspath(__file__))
        )

        try:
            # Create an event loop
            loop = asyncio.get_event_loop()
            # Create a task for running the ros_launch_command
            task = asyncio.create_task(wait_for_process(process))
            print(task)
        except asyncio.CancelledError:
            # The task was cancelled, terminate the process
            process.terminate()
            # Wait for the process to terminate
            await process.wait()
          

        
    @ui.page('/ui')
    def view():
        with ui.header().classes(replace='row items-center') as header:
            with ui.tabs().classes('w-full justify-center') as tabs:
                for tab in tab_list:
                    ui.tab(tab)

        with ui.footer(value=True) as footer:
            ui.label(
                'RoKit testing stack © Fraunhofer IPA 2023').classes('absolute-center items-center')

        with ui.left_drawer(value=True, ).classes('bg-blue-100'):
            ui.label('')

        with ui.right_drawer(value=True).classes('bg-blue-100'):
            ui.label('Hello')
        


        with ui.tab_panels(tabs, value=tab_list[0]):
            with ui.tab_panel(tab_list[1]):
                def add_row():
                    data = api.get_results()
                    max_velocity_table.add_rows({'trial': data[0][1],
                                     'robot name': 'MiR', 
                                     'temperature': 25,
                                     'humidity': 80,
                                     'inclination': 0,
                                     'floor_type': 'wood',
                                     'tracking_object': 'rokit_1',
                                     'notes': 'ambient light was less',
                                     'velocity': data[1][1] })
                    max_velocity_slope_table.add_rows({'trial': data[0][1],
                                     'robot name': 'MiR',
                                     'temperature': 25,
                                     'humidity': 80,
                                     'inclination': 5,
                                     'floor_type': 'wood',
                                     'tracking_object': 'rokit_1',
                                     'notes': 'ambient light was less',
                                     'velocity': data[1][1] })
                columns = [
                    {'name': 'trial', 'label': 'Trial name', 'field': 'trial'},
                    {'name': 'robot name', 'label': 'Robot name', 'field': 'robot name'},
                    {'name': 'temperature','label': 'Temperature(°C)', 'field': 'temperature'},
                    {'name': 'humidity', 'label': 'Humidity(%)', 'field': 'humidity'},
                    {'name': 'inclination', 'label': 'Inclination(degree)', 'field': 'inclination'},
                    {'name': 'tracking_object', 'label': 'Tracking Object', 'field': 'tracking_object'},
                    {'name': 'floor_type', 'label': 'Floor type', 'field': 'floor_type'},
                    {'name': 'notes', 'label': 'Notes', 'field': 'notes'},
                    {'name': 'velocity','label': 'Velocity(m/s)', 'field': 'velocity'},
                ]
                ui.button('REFRESH', on_click=add_row)
                # ui.button('Refresh', on_click=add_row())

                ui.label('MAX_VELOCITY Test Results').classes('text-h4')
                max_velocity_table = ui.table(columns=columns, rows=[],
                                  row_key='trial').classes('w-full my-10')

                ui.label('MAX_VELOCITY_SLOPE Test Results').classes('text-h4')
                max_velocity_slope_table = ui.table(columns=columns, rows=[],
                                  row_key='trial').classes('w-full my-10')

            with ui.tab_panel(tab_list[0]):                
                payload = TestParameters()    
 
                ui.label('Configure the Test').classes('text-h4')

                with ui.row():
                    with ui.column().classes('h-120'):
                        with ui.card().classes('mt-10 mb-1 w-64'):
                            ui.label('Select Test').classes('text-h6')
                            ui.select(test_list, value=test_list[1], on_change=lambda e: frontend_helper.update_test_name(e.value))
                        
                        with ui.card().classes('my-1 w-64'):
                            ui.label('Set Robot details').classes('text-h6')
                            ui.input("robot name", value="MiR", on_change=lambda e: frontend_helper.update_robot_name(e.value))
                        
                        with ui.card().classes('my-1 w-64'):
                            ui.label('Select the tracking object').classes('text-h6')
                            button0 = ui.radio(['tracker_1', 'tracker_2'], value='tracker_1', on_change=lambda: frontend_helper.update_tracking_object(button0.value)).props('inline')
                    
                    with ui.column().classes('h-120'):
                        with ui.card().classes('mt-10 mb-1 w-64'):
                            ui.label('Set environment conditions').classes('text-h6')
                            ui.number("trial_number", value="0", on_change=lambda e: frontend_helper.update_trial_number(e.value))
                            ui.number("temperature", value="0.0", on_change=lambda e: frontend_helper.update_temperature(e.value))
                            ui.number("humidity", value="0.0", on_change=lambda e: frontend_helper.update_humidity(e.value))
                            ui.textarea("notes", value="", on_change=lambda e: frontend_helper.update_notes(e.value))
                    
                    with ui.card().classes('mt-10 w-64'):
                        ui.label('Set testbed conditions').classes('text-h6')
                        ui.number("inclination", value="0.0", on_change=lambda e: frontend_helper.update_inclination(e.value))
                        ui.input("floor type", value="", on_change=lambda e: frontend_helper.update_floor_type(e.value))
                
                with ui.row().classes('mt-10 items-center justify-center'):
                        ui.button('Start Test', on_click=start_app(payload)).classes('mx-2')
                        ui.button('Stop Test', on_click=stop_app).classes('mx-2')
                        
                                        
            with ui.tab_panel(tab_list[2]):
                markdown_content = read_markdown_file(protocols_file_path)
                ui.markdown(markdown_content)

            with ui.tab_panel(tab_list[3]):
                markdown_content = read_markdown_file(conditions_file_path)
                ui.markdown(markdown_content)

    ui.run_with(
        fastapi_app,
        storage_secret='pick your private secret here',
        title='Robot Testing Kit'
    )
