from fastapi import FastAPI
import json
import requests
import random
from nicegui import ui
from nicegui.events import ValueChangeEventArguments

# Define the constants
API_URL = "http://localhost:8001"
conditions_file_path = "rokit_app/static/conditions.md"
protocols_file_path = "rokit_app/static/protocols.md"
TABS = ["Run Tests", "Results", "Test Protocols", "Test Conditions"]
INPUTS_PER_TAB = 5
INPUT_NAMES = ["Temperature", "Humidity",
               "Inclination", "Floor-type", "Notes"]
TESTCASES = ["MAX_VELOCITY", "MAX_VELOCITY_SLOPE"]


def init(fastapi_app: FastAPI) -> None:

    def read_markdown_file(file_path):
        with open(file_path, "r") as f:
            markdown_content = f.read()
        return markdown_content

    def save_parameters(payload):
        response = requests.post(f"{API_URL}/setparams", json=payload)
        print(response.status_code)
        print(response.json())

    def start_test(trial=1):
        response = requests.post(f"{API_URL}/getresults", json=payload)
        print(response.status_code)
        print(response.json())

    def show(event: ValueChangeEventArguments):
        name = type(event.sender).__name__
        ui.notify(f'{name}: {event.value}')

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
        

        input_values = {}
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
                                     'notes': 'ambient light was less',
                                     'velocity': random.uniform(5, 8), })
                    table2.add_rows({'trial': item,
                                    'temperature': 19,
                                     'humidity': 75,
                                     'inclination': 5,
                                     'floortype': 'wood',
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
                    {'name': 'floortype', 'label': 'Floor type', 'field': 'floortype'},
                    {'name': 'notes', 'label': 'Notes', 'field': 'notes'},
                    {'name': 'velocity',
                        'label': 'Velocity(m/s)', 'field': 'velocity'},
                ]

                ui.label('MAX_VELOCITY Test Results').classes('text-h4')
                table1 = ui.table(columns=columns, rows=[],
                                  row_key='trial').classes('w-full my-10')

                ui.label('MAX_VELOCITY_SLOPE Test Results').classes('text-h4')
                table2 = ui.table(columns=columns, rows=[],
                                  row_key='trial').classes('w-full my-10')

            with ui.tab_panel(TABS[0]):
                ui.label('Configure the Test').classes('text-h4')

                with ui.row().classes('items-center'):
                    with ui.card().classes('my-5 h-40'):
                        ui.label('Select Test').classes('text-h6')
                        with ui.element('div').classes('p-2 bg-blue-100'):
                            select0 = ui.select(
                                TESTCASES, value=TESTCASES[0])
                            print(str(select0))
                    with ui.card().classes('my-0 h-40'):
                        ui.label('Select the tracking object').classes(
                            'text-h6')
                        ui.radio(['tracker_1', 'tracker_2'],
                                 value='A', on_change=show).props('inline')

                    with ui.card().classes('my-0 h-120'):
                        ui.label('Set environment conditions').classes(
                            'text-h6')
                        for input_name in INPUT_NAMES:
                            value = ui.input(input_name)
                            input_values[input_name] = value

                payload = {
                    "test_name": "Test Case 1",
                    "temperature": 25.5,
                    "humidity": 60.2,
                    "inclination": 5.7,
                    "floor_type": "Wooden",
                    "notes": "Sample notes"
                }
     # on_click=lambda: ui.notify('Saved parameters!', type='positive',
                with ui.card().classes('my-5'):
                    with ui.row().classes('items-center'):
                        ui.button('Save parameters', on_click=lambda: save_parameters(payload)).classes('items-center')
                        ui.button('Trial 1', on_click=add_row(1))
                        ui.button('Trial 2', on_click=add_row(2))
                        ui.button('Trial 3', on_click=add_row(3))
                        ui.button('Trial 4', on_click=add_row(4))
                        ui.button('Trial 5', on_click=add_row(5))
                        ui.button('Completed', on_click=lambda: ui.colors())


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
