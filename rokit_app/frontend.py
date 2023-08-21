from fastapi import FastAPI
import random
from nicegui import ui
from nicegui.events import ValueChangeEventArguments
from rokit_app.rokitAPI import main as api
from rokit_app.rokitAPI.models import TestParameters, TestResults



# Define the constants
conditions_file_path = "rokit_app/static/conditions.md"
protocols_file_path = "rokit_app/static/protocols.md"
TABS = ["Run Tests", "Results", "Test Protocols", "Test Conditions"]
ID_INPUT = ["trial_number"]
FLOAT_INPUT = ["temperature", "humidity", "inclination", ]
STR_INPUT = ["floor_type", "notes"]
TESTCASES = ["MAX_VELOCITY", "MAX_VELOCITY_SLOPE"]


def init(fastapi_app: FastAPI) -> None:

    def read_markdown_file(file_path):
        with open(file_path, "r") as f:
            markdown_content = f.read()
        return markdown_content

    def show(event: ValueChangeEventArguments):
        name = type(event.sender).__name__
        ui.notify(f'{name}: {event.value}')

    def submit_params(payload):
        # request = TestParameters(**payload)
        # api.set_params(request)
        request = TestParameters(
            test_name=payload["test_name"],
            trial_number=payload["trial_number"],
            tracking_object=payload["tracking_object"],
            temperature=payload["temperature"],
            humidity=payload["humidity"],
            inclination=payload["inclination"],
            floor_type=payload["floor_type"],
            notes=payload["notes"],
        )
        api.set_params(request)



    @ui.page('/ui')
    def view():
        with ui.header().classes(replace='row items-center') as header:
            with ui.tabs().classes('w-full justify-center') as tabs:
                for tab in TABS:
                    ui.tab(tab)

        with ui.footer(value=True) as footer:
            ui.label(
                'RoKit testing stack @ Fraunhofer IPA 2023').classes('absolute-center items-center')

        with ui.left_drawer(value=True, ).classes('bg-blue-100') as left_drawer_0:
            ui.label('')

        with ui.right_drawer(value=True).classes('bg-blue-100') as right_drawer_0:
            ui.label('')
        


        with ui.tab_panels(tabs, value=TABS[0]):
            with ui.tab_panel(TABS[1]):
                #ui.label('Test Results').classes('text-h4 w-full')
                def add_row(key):
                    item = key
                    table1.add_rows({'trial': item,
                                    'temperature': 19,
                                     'humidity': 75,
                                     'inclination': 5,
                                     'floortype': 'wood',
                                     'tracking_object': 'rokit_1',
                                     'notes': 'ambient light was less',
                                     'velocity': random.uniform(5, 8), })
                    table2.add_rows({'trial': item,
                                    'temperature': 19,
                                     'humidity': 75,
                                     'inclination': 5,
                                     'floortype': 'wood',
                                     'tracking_object': 'rokit_2',
                                     'notes': 'ambient light was less',
                                     'velocity': random.uniform(5, 8), })
                columns = [
                    {'name': 'trial', 'label': 'Trial name', 'field': 'trial'},
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
                table1 = ui.table(columns=columns, rows=[],
                                  row_key='trial').classes('w-full my-10')

                ui.label('MAX_VELOCITY_SLOPE Test Results').classes('text-h4')
                table2 = ui.table(columns=columns, rows=[],
                                  row_key='trial').classes('w-full my-10')

            with ui.tab_panel(TABS[0]):                
                payload = {
                    "test_name": "MAX_VELOCITY",    
                    "trial_number": 1,         
                    "tracking_object": "none",     
                    "temperature": 0.0,        
                    "humidity": 0.0,           
                    "inclination": 0.0,        
                    "floor_type": "none",          
                    "notes": "none",               
                }

                def update_payload(name, value):
                    payload[name] = value

                ui.label('Configure the Test').classes('text-h4')

                with ui.row().classes('items-center'):
                    with ui.card().classes('my-5 h-40'):
                        ui.label('Select Test').classes('text-h6')
                        with ui.element('div').classes('p-3 bg-blue-100'):
                            select0 = ui.select(TESTCASES, value=TESTCASES[0])
                            update_payload("test_name", select0.value)
                    with ui.card().classes('my-0 h-40'):
                        ui.label('Select the tracking object').classes(
                            'text-h6')
                        ui.radio(['tracker_1', 'tracker_2'],value='tracker_1', on_change=lambda e: update_payload("tracking_object", str(e.value))).props('inline')

                    with ui.card().classes('my-0 h-120'):
                        ui.label('Set environment conditions').classes(
                            'text-h6')
                        for field_name in ID_INPUT:
                            ui.input(field_name, on_change=lambda e: update_payload(field_name, str(e.value)))

                        for field_name in FLOAT_INPUT:
                            ui.input(field_name, on_change=lambda e: update_payload(field_name, float(e.value)))
                            # value = ui.input(field_name)
                            # payload[field_name] = value

                        for field_name in STR_INPUT:
                            ui.input(field_name, on_change=lambda e: update_payload(field_name, str(e.value)))

                            
                        
                            # value = ui.input(field_name)
                            # payload[field_name] = value

                ## on_click=lambda: ui.notify('Saved parameters!', type='positive',

                def update_trial(number):
                    payload["trial_number"]=int(number)

                with ui.card().classes('my-5'):
                    with ui.row().classes('items-center'):
                        ui.button('Save parameters', on_click=submit_params(payload))
                        ui.button('Start Test', on_click=update_trial(1))
                        # ui.button('Trial 1', on_click=update_trial(1))
                        # ui.button('Trial 2', on_click=update_trial(2))
                        # ui.button('Trial 3', on_click=update_trial(3))
                        # ui.button('Trial 4', on_click=update_trial(4))
                        # ui.button('Trial 5', on_click=update_trial(5))
                        ui.button('Test Result', on_click=lambda: ui.colors())


            with ui.tab_panel(TABS[2]):
                markdown_content = read_markdown_file(protocols_file_path)
                ui.markdown(markdown_content)

            with ui.tab_panel(TABS[3]):
                markdown_content = read_markdown_file(conditions_file_path)
                ui.markdown(markdown_content)

    ui.run_with(
        fastapi_app,
        storage_secret='pick your private secret here',
        title='Robot Testing Kit'
    )
