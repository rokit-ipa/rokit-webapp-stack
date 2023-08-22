from fastapi import FastAPI
import random
from nicegui import ui
from nicegui.events import ValueChangeEventArguments
from rokit_app.rokitAPI import main as api
from rokit_app.rokitAPI.models import TestParameters, TestResults
import shlex
import os
import signal
import asyncio 

# Define the constants
conditions_file_path = "rokit_app/static/conditions.md"
protocols_file_path = "rokit_app/static/protocols.md"
tab_list = ["Run Tests", "Results", "Test Protocols", "Test Conditions"]
test_list = ["MAX_VELOCITY", "MAX_VELOCITY_SLOPE"]
command_start_app = "ros2 launch vicon_calculator.launch.py"
parameter_names = ["robottype", "tracking_object", "trial_number", "temperature", "humidity", "notes", "inclination", "floor type"]
# define some global variables
parameter_list = [None, None, None, None, None, None, None, None, None]
process = None
task = None



def init(fastapi_app: FastAPI) -> None:

    def read_markdown_file(file_path):
        with open(file_path, "r") as f:
            markdown_content = f.read()
        return markdown_content

    def show(event: ValueChangeEventArguments):
        name = type(event.sender).__name__
        ui.notify(f'{name}: {event.value}')

    def submit_params(payload):
        api.set_params(payload)
    
    async def wait_for_process(process):
        await process.wait()
    
    async def stop_app(): 
        print("I want to cancel, but dont do it")
        print(process)
        task.cancel()
        process.send_signal(signal.SIGINT)
    
    async def start_app():
        """Run a command in the background and display the output in the pre-created dialog."""        
        command = command_start_app
        print(parameter_list)
        for i in range(0, 9): 
            command = command + "--" + parameter_names[0] +":=" + str(parameter_list[i])
            
        print("HERE IS PARAMETER LIST")
        print(parameter_list)
        process = await asyncio.create_subprocess_exec(
            *shlex.split(command), cwd=os.path.dirname(os.path.abspath(__file__))
        )

        try:
            # Create an event loop
            loop = asyncio.get_event_loop()
            # Create a task for running the command
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
                'RoKit testing stack @ Fraunhofer IPA 2023').classes('absolute-center items-center')

        with ui.left_drawer(value=True, ).classes('bg-blue-100') as left_drawer_0:
            ui.label('')

        with ui.right_drawer(value=True).classes('bg-blue-100') as right_drawer_0:
            ui.label('')
        


        with ui.tab_panels(tabs, value=tab_list[0]):
            with ui.tab_panel(tab_list[1]):
                def add_row(key):
                    max_velocity_table.add_rows({'trial': key,
                                     'robot name': 'MiR', 
                                     'temperature': 25,
                                     'humidity': 80,
                                     'inclination': 0,
                                     'floor_type': 'wood',
                                     'tracking_object': 'rokit_1',
                                     'notes': 'ambient light was less',
                                     'velocity': random.uniform(0, 1), })
                    max_velocity_slope_table.add_rows({'trial': key,
                                     'robot name': 'MiR',
                                     'temperature': 25,
                                     'humidity': 80,
                                     'inclination': 5,
                                     'floor_type': 'wood',
                                     'tracking_object': 'rokit_2',
                                     'notes': 'ambient light was less',
                                     'velocity': random.uniform(0, 1), })
                columns = [
                    {'name': 'trial', 'label': 'Trial name', 'field': 'trial'},
                    {'name': 'robot name', 'label': 'Robot name', 'field': 'robot name'},
                    {'name': 'temperature',
                        'label': 'Temperature(°C)', 'field': 'temperature'},
                    {'name': 'humidity',
                        'label': 'Humidity(%)', 'field': 'humidity'},
                    {'name': 'inclination',
                        'label': 'Inclination(degree)', 'field': 'inclination'},
                    {'name': 'tracking_object', 'label': 'Tracking Object', 'field': 'tracking_object'},
                    {'name': 'floortype', 'label': 'Floor type', 'field': 'floortype'},
                    {'name': 'notes', 'label': 'Notes', 'field': 'notes'},
                    {'name': 'velocity','label': 'Velocity(m/s)', 'field': 'velocity'},
                ]


                ui.label('MAX_VELOCITY Test Results').classes('text-h4')
                max_velocity_table = ui.table(columns=columns, rows=[],
                                  row_key='trial').classes('w-full my-10')

                ui.label('MAX_VELOCITY_SLOPE Test Results').classes('text-h4')
                max_velocity_slope_table = ui.table(columns=columns, rows=[],
                                  row_key='trial').classes('w-full my-10')

                add_row(1)
                add_row(2)

            with ui.tab_panel(tab_list[0]):                
                payload = TestParameters()    
 
                ui.label('Configure the Test').classes('text-h4')

                with ui.row():
                    with ui.column().classes('h-120'):
                        #ui.label("__________________________________________________________________________________________________________________________________________________________________")
                        with ui.card().classes('mt-10 mb-1 w-64'):
                            ui.label('Select Test').classes('text-h6')
                            ui.select(test_list, value=test_list[1], on_change=lambda e: update_value(e.value,0))
                        
                        with ui.card().classes('my-1 w-64'):
                            ui.label('Set Robot details').classes('text-h6')
                            ui.input("robot name", value="MiR", on_change=lambda e: update_value(e.value, 1))
                        
                        with ui.card().classes('my-1 w-64'):
                            ui.label('Select the tracking object').classes('text-h6')
                            button0 = ui.radio(['tracker_1', 'tracker_2'], value='tracker_1', on_change=lambda: update_value(button0.value, 2)).props('inline')
                    
                    with ui.column().classes('h-120'):
                        with ui.card().classes('mt-10 mb-1 w-64'):
                            ui.label('Set environment conditions').classes('text-h6')
                            ui.number("trial_number", value="0", on_change=lambda e: update_value(e.value, 3))
                            ui.number("temperature", value="0.0", on_change=lambda e: update_value(e.value, 4))
                            ui.number("humidity", value="0.0", on_change=lambda e: update_value(e.value, 5))
                            ui.textarea("notes", value="", on_change=lambda e: update_value(e.value, 6))
                    
                    with ui.card().classes('mt-10 w-64'):
                        ui.label('Set testbed conditions').classes('text-h6')
                        ui.number("inclination", value="0.0", on_change=lambda e: update_value(e.value, 7))
                        ui.input("floor type", value="", on_change=lambda e: update_value(e.value, 8))
                
                with ui.row().classes('mt-10 items-center justify-center'):
                        ui.button('Start Test', on_click=start_app).classes('mx-2')
                        ui.button('Stop Test', on_click=stop_app).classes('mx-2')
                        
                def update_value(selected_value, index):
                    payload.robot_name=selected_value 
                    parameter_list[index] = selected_value
                            
                        
                                           
            with ui.tab_panel(tab_list[2]):
                markdown_content = read_markdown_file(protocols_file_path)
                #ui.markdown('''markdown_content''')

            with ui.tab_panel(tab_list[3]):
                markdown_content = read_markdown_file(conditions_file_path)
                #ui.markdown(markdown_content)

    ui.run_with(
        fastapi_app,
        storage_secret='pick your private secret here',
        title='Robot Testing Kit'
    )
